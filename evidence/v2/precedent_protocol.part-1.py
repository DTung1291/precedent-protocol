# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
"""Precedent Protocol: precedent-aware semantic arbitration.

Two named parties submit arguments and content-addressed public evidence. A
leader produces a five-lens deliberation panel and explicit treatment of prior
cases. Validators independently fetch the same evidence and produce their own
panel. Only a consensus-compatible verdict reaches the append-only round
ledger. Later reviews may affirm or reverse the current result without erasing
history.

This is an agreed arbitration primitive, not a legal court and not a wrapper
around GenLayer's protocol-level transaction appeals.
"""
from genlayer import *

import hashlib
import json
import re
from datetime import datetime
from urllib.parse import urlsplit


MAX_OUTCOMES = 4
MAX_EVIDENCE_PER_SUBMISSION = 6
MAX_TOTAL_EVIDENCE = 10
MAX_EVIDENCE_BYTES = 16000
MAX_TOTAL_BYTES = 60000
MAX_PRECEDENTS = 5
MAX_ROUNDS = 3
PANEL_SIZE = 5
# A substantive five-lens majority can only produce 0, 200, or 400. Once
# validators agree on the verdict and every precedent relation, differences
# inside that full majority-strength band are equivalent for consensus.
SUBSTANTIVE_CONTESTABILITY_BAND = 400
LENSES = ("FACTS", "POLICY", "ADVERSARIAL", "PRECEDENT", "REMEDY")
RELATIONS = ("APPLY", "DISTINGUISH", "CONFLICT", "IRRELEVANT")


def _revert(message):
    raise gl.vm.UserError(message)


def _timestamp():
    value = gl.message_raw["datetime"].replace("Z", "+00:00")
    return int(datetime.fromisoformat(value).timestamp())


def _address(value):
    if isinstance(value, int):
        if value < 0 or value >= 2 ** 160:
            _revert("address out of range")
        return f"0x{value:040x}"
    return value.as_hex.lower()


def _address_text(value, label):
    if not isinstance(value, str) or not re.fullmatch(r"0x[0-9a-fA-F]{40}", value):
        _revert(f"{label}: invalid address")
    result = value.lower()
    if result == "0x" + "0" * 40:
        _revert(f"{label}: zero address")
    return result


def _text(value, label, cap, allow_empty=False):
    if not isinstance(value, str) or len(value) > cap:
        _revert(f"{label}: invalid length")
    value = value.strip()
    if not allow_empty and not value:
        _revert(f"{label}: empty")
    if any(ord(ch) < 32 and ch not in "\n\t" for ch in value):
        _revert(f"{label}: control character")
    return value


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _digest(value):
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _parse_json(raw, label, cap):
    if not isinstance(raw, str) or len(raw) > cap:
        _revert(f"{label}: invalid length")
    try:
        return json.loads(raw)
    except Exception:
        _revert(f"{label}: invalid JSON")


def _evidence_manifest(raw, label, cap=MAX_EVIDENCE_PER_SUBMISSION):
    rows = _parse_json(raw, label, 8000)
    if not isinstance(rows, list) or len(rows) > cap:
        _revert(f"{label}: expected at most {cap} items")
    clean = []
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"url", "sha256", "label"}:
            _revert(f"{label}: each item needs url, sha256, and label")
        url = _text(row["url"], "evidence url", 700)
        parsed = urlsplit(url)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
            _revert("evidence url: public HTTPS required")
        if parsed.port is not None and parsed.port != 443:
            _revert("evidence url: nonstandard port")
        if parsed.fragment:
            _revert("evidence url: fragments are not allowed")
        sha = str(row["sha256"]).lower()
        if not re.fullmatch(r"[0-9a-f]{64}", sha):
            _revert("evidence sha256: 64 lowercase hex characters required")
        item = {"url": url, "sha256": sha, "label": _text(row["label"], "evidence label", 120)}
        key = f"{url}:{sha}"
        if key in seen:
            _revert(f"{label}: duplicate evidence")
        seen.add(key)
        clean.append(item)
    return clean


def _fetch_body(response, item):
    status = getattr(response, "status_code", getattr(response, "status", None))
    if status != 200:
        raise ValueError(f"evidence HTTP status {status}")
    raw = response.body
    if isinstance(raw, bytes):
        body = raw
    else:
        body = str(raw).encode("utf-8")
    if len(body) > MAX_EVIDENCE_BYTES:
        raise ValueError("evidence exceeds per-item byte limit")
    if hashlib.sha256(body).hexdigest() != item["sha256"]:
        raise ValueError("evidence content hash mismatch")
    return body.decode("utf-8", errors="replace")


def _fallback_panel(reason, basis_status):
    reason = str(reason)[:300]
    return {
        "basis_status": basis_status,
        "verdict": "ABSTAIN",
        "contestability_milli": 1000,
        "opinions": [
            {"lens": lens, "verdict": "ABSTAIN", "reason": reason}
            for lens in LENSES
        ],
        "precedent_treatments": [],
        "summary": reason,
        "missing_information": reason,
        "strongest_counterargument": "A safe substantive verdict could not be established.",
    }


def _unwrap_json(value):
    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            start, end = value.find("{"), value.rfind("}")
            if start >= 0 and end > start:
                try:
                    return json.loads(value[start:end + 1])
                except Exception:
                    return None
            return None
    if isinstance(value, dict) and "opinions" not in value:
        for key in ("result", "response", "data"):
            if isinstance(value.get(key), (dict, str)):
                return _unwrap_json(value[key])
    return value


def _normalise_panel(value, outcomes, precedent_ids):
    value = _unwrap_json(value)
    if isinstance(value, dict) and value.get("basis_status") in (
        "EVIDENCE_UNAVAILABLE", "MODEL_OUTPUT_INVALID"
    ):
        # Canonical fallbacks are contract-generated, never accepted as a
        # substantive result. Rebuild them so representation extras cannot
        # cross the consensus boundary. Validators still independently fetch
        # evidence below before accepting EVIDENCE_UNAVAILABLE.
        return _fallback_panel(
            str(value.get("summary", "safe abstention")), value["basis_status"]
        )
    required = {
        "opinions", "precedent_treatments", "summary",
        "missing_information", "strongest_counterargument",
    }
    if not isinstance(value, dict) or not required.issubset(value):
        return _fallback_panel("model output was malformed", "MODEL_OUTPUT_INVALID")
    allowed = tuple(outcomes) + ("ABSTAIN",)
    opinions = value["opinions"]
    if not isinstance(opinions, list) or len(opinions) != PANEL_SIZE:
        return _fallback_panel("model panel was incomplete", "MODEL_OUTPUT_INVALID")
    clean_opinions = []
    seen_lenses = set()
    for row in opinions:
        if not isinstance(row, dict) or not {"lens", "verdict", "reason"}.issubset(row):
            return _fallback_panel("model opinion was malformed", "MODEL_OUTPUT_INVALID")
        lens = str(row["lens"]).strip().upper()
        verdict = str(row["verdict"]).strip().upper()
        reason = row["reason"]
        if lens not in LENSES or lens in seen_lenses or verdict not in allowed:
            return _fallback_panel("model opinion used an invalid lens or verdict", "MODEL_OUTPUT_INVALID")
        if not isinstance(reason, str) or not reason.strip():
            return _fallback_panel("model opinion lacked reasoning", "MODEL_OUTPUT_INVALID")
        seen_lenses.add(lens)
        clean_opinions.append({"lens": lens, "verdict": verdict, "reason": reason.strip()[:320]})
    if seen_lenses != set(LENSES):
        return _fallback_panel("model panel omitted a required lens", "MODEL_OUTPUT_INVALID")

    counts = {name: 0 for name in allowed}
    for row in clean_opinions:
        counts[row["verdict"]] += 1
    ranked = sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))
    winner, winner_count = ranked[0]
    tied = len(ranked) > 1 and ranked[1][1] == winner_count
    verdict = winner if winner_count >= 3 and not tied and winner != "ABSTAIN" else "ABSTAIN"
    contestability = 1000 if verdict == "ABSTAIN" else 1000 - winner_count * 200

    treatments = value["precedent_treatments"]
    if not isinstance(treatments, list):
        return _fallback_panel("precedent treatments were malformed", "MODEL_OUTPUT_INVALID")
    clean_treatments = []
    seen_ids = set()
    for row in treatments:
        if not isinstance(row, dict) or not {"case_id", "relation", "reason"}.issubset(row):
            return _fallback_panel("precedent treatment was malformed", "MODEL_OUTPUT_INVALID")
        try:
            case_id = int(str(row["case_id"]).strip())
        except Exception:
            return _fallback_panel("precedent id was malformed", "MODEL_OUTPUT_INVALID")
        relation = str(row["relation"]).strip().upper()
        reason = row["reason"]
        if case_id not in precedent_ids or case_id in seen_ids or relation not in RELATIONS:
            return _fallback_panel("precedent treatment was invalid", "MODEL_OUTPUT_INVALID")
        if not isinstance(reason, str) or not reason.strip():
            return _fallback_panel("precedent treatment lacked reasoning", "MODEL_OUTPUT_INVALID")
        seen_ids.add(case_id)
        clean_treatments.append({"case_id": case_id, "relation": relation, "reason": reason.strip()[:320]})
    if seen_ids != set(precedent_ids):
        return _fallback_panel("not every submitted precedent was addressed", "MODEL_OUTPUT_INVALID")
    clean_treatments.sort(key=lambda row: row["case_id"])

    strings = []
    for key, cap in (("summary", 600), ("missing_information", 400), ("strongest_counterargument", 400)):
        item = value[key]
        if not isinstance(item, str) or not item.strip():
            return _fallback_panel(f"{key} was missing", "MODEL_OUTPUT_INVALID")
        strings.append(item.strip()[:cap])
    return {
        "basis_status": "OK",
        "verdict": verdict,
        "contestability_milli": contestability,
        "opinions": clean_opinions,
        "precedent_treatments": clean_treatments,
        "summary": strings[0],
        "missing_information": strings[1],
        "strongest_counterargument": strings[2],
    }


def _relation_vector(panel):
    return [(row["case_id"], row["relation"]) for row in panel["precedent_treatments"]]


class PrecedentProtocol(gl.Contract):
    policy_count: u32
    case_count: u32
    round_count: u32
    policies_json: TreeMap[u32, str]
    cases_json: TreeMap[u32, str]
    rounds_json: TreeMap[u32, str]
    case_rounds_json: TreeMap[u32, str]
    case_dedupe: TreeMap[str, u32]
    round_dedupe: TreeMap[str, u32]

    def __init__(self):
        self.policy_count = u32(0)
        self.case_count = u32(0)
        self.round_count = u32(0)

    def _load(self, store, item_id, count, label):
        if not isinstance(item_id, int) or item_id < 1 or item_id > int(count):
            _revert(f"{label} not found")
        raw = store.get(u32(item_id), "")
        if not raw:
            _revert(f"{label} not found")
        return json.loads(raw)

    @gl.public.write
    def create_policy(self, name: str, standard: str, outcomes_json: str) -> int:
        name = _text(name, "name", 100)
        standard = _text(standard, "standard", 2400)
        outcomes = _parse_json(outcomes_json, "outcomes_json", 1000)
        if not isinstance(outcomes, list) or not 2 <= len(outcomes) <= MAX_OUTCOMES:
            _revert("outcomes_json: expected 2-4 outcomes")
        clean = []
        for value in outcomes:
            outcome = str(value).strip().upper()
            if not re.fullmatch(r"[A-Z][A-Z0-9_]{1,31}", outcome) or outcome == "ABSTAIN":
                _revert("outcome: invalid label")
            if outcome in clean:
                _revert("outcome: duplicate label")
            clean.append(outcome)
        policy_id = int(self.policy_count) + 1
        policy = {
            "id": policy_id,
            "owner": _address(gl.message.sender_address),
            "name": name,
            "standard": standard,
            "outcomes": clean,
            "policy_hash": _digest({"standard": standard, "outcomes": clean}),
            "created_at": _timestamp(),
        }
        self.policies_json[u32(policy_id)] = _canonical(policy)
        self.policy_count = u32(policy_id)
        return policy_id

    @gl.public.write
    def open_case(
        self,
        policy_id: int,
        respondent_address: str,
        question: str,
        claimant_statement: str,
        evidence_json: str,
    ) -> int:
        policy = self._load(self.policies_json, policy_id, self.policy_count, "policy")
        claimant = _address(gl.message.sender_address)
        respondent = _address_text(respondent_address, "respondent_address")
        if respondent == claimant:
            _revert("respondent must differ from claimant")
        question = _text(question, "question", 900)
        statement = _text(claimant_statement, "claimant_statement", 3500)
        evidence = _evidence_manifest(evidence_json, "evidence_json")
        fingerprint = _digest({
            "policy_hash": policy["policy_hash"], "claimant": claimant,
            "respondent": respondent, "question": question,
        })
        if int(self.case_dedupe.get(fingerprint, u32(0))) != 0:
            _revert("duplicate case")
        case_id = int(self.case_count) + 1
        record = {
            "id": case_id,
            "policy_id": policy_id,
            "policy_hash": policy["policy_hash"],
            "claimant": claimant,
            "respondent": respondent,
            "question": question,
            "claimant_statement": statement,
            "claimant_evidence": evidence,
            "respondent_statement": "",
            "respondent_evidence": [],
            "status": "AWAITING_RESPONSE",
            "current_verdict": "",
            "current_contestability_milli": 0,
            "current_round_id": 0,
            "round_count": 0,
            "created_at": _timestamp(),
        }
        self.cases_json[u32(case_id)] = _canonical(record)
        self.case_rounds_json[u32(case_id)] = "[]"
        self.case_dedupe[fingerprint] = u32(case_id)
        self.case_count = u32(case_id)
        return case_id

    @gl.public.write
    def submit_response(self, case_id: int, respondent_statement: str, evidence_json: str):
        case = self._load(self.cases_json, case_id, self.case_count, "case")
        if _address(gl.message.sender_address) != case["respondent"]:
            _revert("only the named respondent may respond")
        if cas