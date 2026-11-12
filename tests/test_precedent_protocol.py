"""Deterministic and consensus-boundary tests for Precedent Protocol."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import types
import unittest


CLAIMANT = "0x1111111111111111111111111111111111111111"
RESPONDENT = "0x2222222222222222222222222222222222222222"
OUTSIDER = "0x3333333333333333333333333333333333333333"


class UserError(Exception):
    pass


class ConsensusDisagreement(Exception):
    pass


class Return:
    def __init__(self, calldata):
        self.calldata = calldata


class Address:
    def __init__(self, value):
        self.as_hex = value.lower()


class Runtime:
    def __init__(self):
        self.sender = Address(CLAIMANT)
        self.prompt_results = []
        self.prompts = []
        self.web_requests = []
        self.bodies = {"https://evidence.example/item": b"Signed delivery record: accepted."}
        self.statuses = {}

    def web_request(self, url, method="GET"):
        self.web_requests.append((url, method))
        status = self.statuses.get(url, 200)
        return types.SimpleNamespace(status_code=status, body=self.bodies.get(url, b""))

    def exec_prompt(self, prompt, response_format=None):
        self.prompts.append(prompt)
        if response_format != "json":
            raise AssertionError("contract must request JSON output")
        if not self.prompt_results:
            raise AssertionError("missing prompt result")
        return self.prompt_results.pop(0)

    def run_nondet_unsafe(self, leader_fn, validator_fn):
        candidate = leader_fn()
        if not validator_fn(Return(candidate)):
            raise ConsensusDisagreement("validator rejected leader result")
        return candidate


def load_contract(runtime):
    module = types.ModuleType("genlayer")

    class Public:
        @staticmethod
        def write(fn):
            return fn

        @staticmethod
        def view(fn):
            return fn

    class Contract:
        pass

    class U32(int):
        pass

    class TreeMap(dict):
        @classmethod
        def __class_getitem__(cls, _item):
            return cls

    gl = types.SimpleNamespace(
        Contract=Contract,
        public=Public(),
        message=types.SimpleNamespace(sender_address=runtime.sender),
        message_raw={"datetime": "2026-11-11T08:00:00+00:00"},
        nondet=types.SimpleNamespace(
            web=types.SimpleNamespace(request=runtime.web_request),
            exec_prompt=runtime.exec_prompt,
        ),
        vm=types.SimpleNamespace(
            UserError=UserError,
            Return=Return,
            run_nondet_unsafe=runtime.run_nondet_unsafe,
        ),
    )
    module.gl = gl
    module.u32 = U32
    module.TreeMap = TreeMap
    module.__all__ = ["gl", "u32", "TreeMap"]
    sys.modules["genlayer"] = module
    path = Path(__file__).parents[1] / "contracts" / "precedent_protocol.py"
    spec = importlib.util.spec_from_file_location("precedent_protocol_under_test", path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded, gl


def make_panel(winner="CLAIMANT", minority="RESPONDENT", winner_count=4, precedents=()):
    verdicts = [winner] * winner_count + [minority] * (5 - winner_count)
    opinions = [
        {"lens": lens, "verdict": verdicts[index], "reason": f"{lens} supports {verdicts[index]}."}
        for index, lens in enumerate(("FACTS", "POLICY", "ADVERSARIAL", "PRECEDENT", "REMEDY"))
    ]
    return {
        "opinions": opinions,
        "precedent_treatments": [
            {"case_id": value, "relation": "APPLY", "reason": "The material issue matches."}
            for value in precedents
        ],
        "summary": "The panel reached a bounded semantic decision.",
        "missing_information": "No material omission changed the majority.",
        "strongest_counterargument": "The minority reads the evidence differently.",
    }


def make_audit(failed=None):
    checks = (
        "EVIDENCE_SUPPORT",
        "POLICY_APPLICATION",
        "COUNTERARGUMENT_FAIRNESS",
        "PRECEDENT_RELATIONS",
        "VERDICT_DERIVATION",
    )
    return {
        "checks": [
            {
                "check": check,
                "passed": check != failed,
                "reason": "The proposed report satisfies this bounded proof obligation."
                if check != failed else "The proposed report is unsupported on this obligation.",
            }
            for check in checks
        ]
    }


class PrecedentProtocolTests(unittest.TestCase):
    def setUp(self):
        self.runtime = Runtime()
        self.module, self.gl = load_contract(self.runtime)
        self.contract = self.module.PrecedentProtocol()
        self.contract.policies_json = {}
        self.contract.cases_json = {}
        self.contract.rounds_json = {}
        self.contract.case_rounds_json = {}
        self.contract.case_dedupe = {}
        self.contract.round_dedupe = {}

    def set_sender(self, address):
        self.runtime.sender = Address(address)
        self.gl.message.sender_address = self.runtime.sender

    def create_policy(self, outcomes=("CLAIMANT", "RESPONDENT"), name="Delivery policy"):
        return self.contract.create_policy(
            name,
            "Choose the party whose position is best supported by the bounded evidence.",
            json.dumps(list(outcomes)),
        )

    def evidence(self, correct=True, url="https://evidence.example/item"):
        body = self.runtime.bodies.get(url, b"")
        digest = hashlib.sha256(body).hexdigest() if correct else "0" * 64
        return json.dumps([{"url": url, "sha256": digest, "label": "Delivery record"}])

    def open_ready_case(self, policy_id=None, claimant_evidence="[]", respondent_evidence="[]", question="Was delivery accepted?"):
        policy_id = policy_id or self.create_policy()
        self.set_sender(CLAIMANT)
        case_id = self.contract.open_case(
            policy_id, RESPONDENT, question, "The delivery satisfied the agreed specification.", claimant_evidence
        )
        self.set_sender(RESPONDENT)
        self.contract.submit_response(
            case_id, "The delivery did not satisfy the agreed specification.", respondent_evidence
        )
        return case_id

    def decide(self, case_id, leader=None, validator=None, note="", review_evidence="[]", precedents=()):
        self.runtime.prompt_results = [leader or make_panel(), validator or make_audit()]
        return self.contract.decide(case_id, note, review_evidence, json.dumps(list(precedents)))

    def test_policy_is_immutable_content_addressed_state(self):
        policy_id = self.create_policy()
        policy = self.contract.get_policy(policy_id)
        self.assertEqual(policy["owner"], CLAIMANT)
        self.assertEqual(policy["outcomes"], ["CLAIMANT", "RESPONDENT"])
        self.assertEqual(len(policy["policy_hash"]), 64)
        self.assertEqual(self.contract.get_policy_count(), 1)

    def test_policy_rejects_bad_outcomes(self):
        bad = ["[]", '["ONLY"]', '["A","A"]', '["ABSTAIN","YES"]', '["bad label","YES"]']
        for raw in bad:
            with self.subTest(raw=raw), self.assertRaises(UserError):
                self.contract.create_policy("P", "S", raw)

    def test_case_names_both_parties_and_requires_response(self):
        policy_id = self.create_policy()
        case_id = self.contract.open_case(policy_id, RESPONDENT, "Question", "Claim", "[]")
        case = self.contract.get_case(case_id)
        self.assertEqual(case["status"], "AWAITING_RESPONSE")
        self.assertEqual(case["claimant"], CLAIMANT)
        self.assertEqual(case["respondent"], RESPONDENT)
        with self.assertRaises(UserError):
            self.contract.decide(case_id, "", "[]", "[]")

    def test_case_dedupes_same_policy_parties_and_question(self):
        policy_id = self.create_policy()
        self.contract.open_case(policy_id, RESPONDENT, "Question", "Claim", "[]")
        with self.assertRaises(UserError):
            self.contract.open_case(policy_id, RESPONDENT, "Question", "Different prose", "[]")

    def test_only_named_respondent_can_respond_once(self):
        policy_id = self.create_policy()
        case_id = self.contract.open_case(policy_id, RESPONDENT, "Question", "Claim", "[]")
        self.set_sender(OUTSIDER)
        with self.assertRaises(UserError):
            self.contract.submit_response(case_id, "Response", "[]")
        self.set_sender(RESPONDENT)
        self.contract.submit_response(case_id, "Response", "[]")
        with self.assertRaises(UserError):
            self.contract.submit_response(case_id, "Second response", "[]")

    def test_initial_decision_derives_verdict_and_contestability(self):
        case_id = self.open_ready_case()
        self.set_sender(CLAIMANT)
        round_id = self.decide(case_id)
        case = self.contract.get_case(case_id)
        record = self.contract.get_round(round_id)
        self.assertEqual(case["current_verdict"], "CLAIMANT")
        self.assertEqual(case["current_contestability_milli"], 200)
        self.assertEqual(record["report"]["verdict"], "CLAIMANT")
        self.assertEqual(self.contract.get_case_rounds(case_id), [round_id])

    def test_split_panel_abstains_instead_of_guessing(self):
        case_id = self.open_ready_case(outcomes := self.create_policy(("CLAIMANT", "RESPONDENT", "SPLIT")))
        leader = make_panel("CLAIMANT", "RESPONDENT", 2)
        leader["opinions"][-1]["verdict"] = "SPLIT"
        self.set_sender(CLAIMANT)
        round_id = self.decide(case_id, leader)
        report = self.contract.get_round(round_id)["report"]
        self.assertEqual(report["verdict"], "ABSTAIN")
        self.assertEqual(report["contestability_milli"], 1000)

    def test_outsider_cannot_request_decision(self):
        case_id = self.open_ready_case()
        self.set_sender(OUTSIDER)
        with self.assertRaises(UserError):
            self.decide(case_id)

    def test_failed_validator_proof_obligation_prevents_state_write(self):
        case_id = self.open_ready_case()
        self.set_sender(CLAIMANT)
        with self.assertRaises(ConsensusDisagreement):
            self.decide(case_id, make_panel("CLAIMANT"), make_audit("EVIDENCE_SUPPORT"))
        self.assertEqual(self.contract.get_round_count(), 0)
        self.assertEqual(self.contract.get_case(case_id)["status"], "READY")

    def test_valid_proof_audit_accepts_deterministically_derived_majority(self):
        case_id = self.open_ready_case()
        self.set_sender(CLAIMANT)
        round_id = self.decide(case_id, make_panel(winner_count=5), make_audit())
        report = self.contract.get_round(round_id)["report"]
        self.assertEqual(report["verdict"], "CLAIMANT")
        self.assertEqual(report["contestability_milli"], 0)

    def test_malformed_leader_panel_cannot_be_approved_by_valid_validator(self):
        case_id = self.open_ready_case()
        self.set_sender(CLAIMANT)
        with self.assertRaises(ConsensusDisagreement):
            self.decide(case_id, {"verdict": "CLAIMANT"}, make_audit())

    def test_malformed_validator_audit_prevents_state_write(self):
        case_id = self.open_ready_case()
        self.set_sender(CLAIMANT)
        with self.assertRaises(ConsensusDisagreement):
            self.decide(case_id, validator={"checks": []})
        self.assertEqual(self.contract.get_round_count(), 0)

    def test_content_hash_failure_fails_closed_to_abstain(self):
        case_id = self.open_ready_case(claimant_evidence=self.evidence(correct=False))
        self.set_sender(CLAIMANT)
        self.runtime.prompt_results = []
        round_id = self.contract.decide(case_id, "", "[]", "[]")
        report = self.contract.get_round(round_id)["report"]
        self.assertEqual(report["verdict"], "ABSTAIN")
        self.assertEqual(report["basis_status"], "EVIDENCE_UNAVAILABLE")

    def test_http_failure_fails_closed_to_abstain(self):
        url = "https://evidence.example/item"
        self.runtime.statuses[url] = 503
        case_id = self.open_ready_case(claimant_evidence=self.evidence())
        self.set_sender(CLAIMANT)
        self.runtime.prompt_results = []
        round_id = self.contract.decide(case_id, "", "[]", "[]")
        self.assertEqual(self.contract.get_round(round_id)["report"]["verdict"], "ABSTAIN")

    def test_evidence_is_hash_bound_and_treated_as_untrusted(self):
        case_id = self.open_ready_case(claimant_evidence=self.evidence())
        self.set_sender(CLAIMANT)
        self.decide(case_id)
        self.assertEqual(len(self.runtime.web_requests), 2)
        self.assertTrue(all(method == "GET" for _, method in self.runtime.web_requests))
        self.assertIn("untrusted", self.runtime.prompts[0].lower())
        self.assertIn("untrusted", self.runtime.prompts[1].lower())

    def test_precedent_must_be_resolved_under_same_policy(self):
        policy_id = self.create_policy()
        unresolved = self.contract.open_case(policy_id, RESPONDENT, "Old question", "Old claim", "[]")
        current = self.open_ready_case(policy_id, question="New question")
        self.set_sender(CLAIMANT)
        with self.assertRaises(UserError):
            self.decide(current, precedents=(unresolved,))
        other_policy = self.create_policy(name="Other")
        foreign = self.open_ready_case(other_policy, question="Foreign question")
        self.decide(foreign)
        self.set_sender(CLAIMANT)
        with self.assertRaises(UserError):
            self.decide(current, precedents=(foreign,))

    def test_unsupported_precedent_relation_prevents_write(self):
        policy_id = self.create_policy()
        prior = self.open_ready_case(policy_id, question="Prior question")
        self.set_sender(CLAIMANT)
        self.decide(prior)
        current = self.open_ready_case(policy_id, question="Current question")
        leader = make_panel(precedents=(prior,))
        self.set_sender(CLAIMANT)
        with self.assertRaises(ConsensusDisagreement):
            self.decide(current, leader, make_audit("PRECEDENT_RELATIONS"), precedents=(prior,))

    def test_review_is_append_only_and_can_reverse_current_verdict(self):
        case_id = self.open_ready_case()
        self.set_sender(CLAIMANT)
        first = self.decide(case_id)
        second = self.decide(
            case_id,
            make_panel("RESPONDENT", "CLAIMANT"),
            make_audit(),
            note="The first round overlooked the acceptance timestamp.",
        )
        case = self.contract.get_case(case_id)
        self.assertEqual(case["current_verdict"], "RESPONDENT")
        self.assertEqual(case["current_round_id"], second)
        self.assertEqual(self.contract.get_case_rounds(case_id), [first, second])
        self.assertEqual(self.contract.get_round(first)["report"]["verdict"], "CLAIMANT")
        self.assertEqual(self.contract.get_round(second)["prior_round_id"], first)

    def test_review_requires_note_and_is_limited_to_three_rounds(self):
        case_id = self.open_ready_case()
        self.set_sender(CLAIMANT)
        self.decide(case_id)
        with self.assertRaises(UserError):
            self.decide(case_id)
        self.decide(case_id, note="Challenge one")
        self.decide(case_id, note="Challenge two")
        with self.assertRaises(UserError):
            self.decide(case_id, note="Challenge three")

    def test_round_hash_binds_prior_state_and_review_challenge(self):
        case_id = self.open_ready_case()
        self.set_sender(CLAIMANT)
        first = self.decide(case_id)
        second = self.decide(case_id, note="Material timestamp was overlooked")
        first_record = self.contract.get_round(first)
        second_record = self.contract.get_round(second)
        self.assertNotEqual(first_record["request_hash"], second_record["request_hash"])
        self.assertEqual(second_record["prior_round_id"], first)
        self.assertEqual(len(first_record["request_hash"]), 64)

    def test_invalid_evidence_urls_and_hashes_are_rejected(self):
        policy_id = self.create_policy()
        bad = [
            [{"url": "http://example.com", "sha256": "a" * 64, "label": "x"}],
            [{"url": "https://user:pass@example.com/x", "sha256": "a" * 64, "label": "x"}],
            [{"url": "https://example.com/x#fragment", "sha256": "a" * 64, "label": "x"}],
            [{"url": "https://example.com/x", "sha256": "short", "label": "x"}],
        ]
        for value in bad:
            with self.subTest(value=value), self.assertRaises(UserError):
                self.contract.open_case(policy_id, RESPONDENT, "Q", "C", json.dumps(value))

    def test_missing_views_revert(self):
        with self.assertRaises(UserError):
            self.contract.get_policy(1)
        with self.assertRaises(UserError):
            self.contract.get_case(1)
        with self.assertRaises(UserError):
            self.contract.get_round(1)


if __name__ == "__main__":
    unittest.main()
