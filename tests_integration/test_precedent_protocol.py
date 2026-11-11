"""Official gltest integration checks for Precedent Protocol.

Run against a validator-backed network:

    gltest --network studionet tests_integration/test_precedent_protocol.py

Assertions pin state-machine and consensus invariants, never exact model prose.
"""
import json

from gltest import create_account, get_contract_factory
from gltest.assertions import tx_execution_succeeded


def _deploy():
    return get_contract_factory("PrecedentProtocol").deploy()


def _object(value):
    return json.loads(value) if isinstance(value, str) else value


def _create_policy(contract):
    receipt = contract.create_policy(
        args=[
            "Acknowledged delivery",
            (
                "Evaluate the complete record. Choose CLAIMANT only when the "
                "respondent clearly acknowledges that the described delivery "
                "occurred; choose RESPONDENT only when the record clearly "
                "establishes it did not occur; otherwise abstain."
            ),
            '["CLAIMANT","RESPONDENT"]',
        ]
    ).transact()
    assert tx_execution_succeeded(receipt)
    return 1


def _open_ready_case(contract, respondent, question):
    receipt = contract.open_case(
        args=[
            1,
            respondent.address,
            question,
            "The delivery occurred and was acknowledged by both parties.",
            "[]",
        ]
    ).transact()
    assert tx_execution_succeeded(receipt)
    case_id = contract.get_case_count().call()
    receipt = contract.connect(account=respondent).submit_response(
        args=[
            case_id,
            "I acknowledge that the delivery described by the claimant occurred.",
            "[]",
        ]
    ).transact()
    assert tx_execution_succeeded(receipt)
    return case_id


def test_deploys_empty():
    contract = _deploy()
    assert contract.get_policy_count().call() == 0
    assert contract.get_case_count().call() == 0
    assert contract.get_round_count().call() == 0


def test_two_party_state_machine_enforces_named_respondent():
    contract = _deploy()
    _create_policy(contract)
    respondent = create_account()
    outsider = create_account()
    receipt = contract.open_case(
        args=[1, respondent.address, "Was the package delivered?", "Yes.", "[]"]
    ).transact()
    assert tx_execution_succeeded(receipt)

    rejected = contract.connect(account=outsider).submit_response(
        args=[1, "Unauthorized response", "[]"]
    ).transact()
    assert not tx_execution_succeeded(rejected)

    accepted = contract.connect(account=respondent).submit_response(
        args=[1, "The package was delivered.", "[]"]
    ).transact()
    assert tx_execution_succeeded(accepted)
    case = _object(contract.get_case(args=[1]).call())
    assert case["status"] == "READY"
    assert case["respondent"].lower() == respondent.address.lower()


def test_clear_case_writes_bounded_consensus_round():
    contract = _deploy()
    _create_policy(contract)
    respondent = create_account()
    case_id = _open_ready_case(
        contract, respondent, "Did the respondent acknowledge the delivery?"
    )

    receipt = contract.decide(args=[case_id, "", "[]", "[]"]).transact()
    assert tx_execution_succeeded(receipt)

    case = _object(contract.get_case(args=[case_id]).call())
    record = _object(contract.get_round(args=[case["current_round_id"]]).call())
    report = record["report"]
    assert case["status"] == "RESOLVED"
    assert report["verdict"] in ("CLAIMANT", "RESPONDENT", "ABSTAIN")
    assert report["contestability_milli"] in (0, 200, 400, 1000)
    assert len(report["opinions"]) == 5
    assert {row["lens"] for row in report["opinions"]} == {
        "FACTS", "POLICY", "ADVERSARIAL", "PRECEDENT", "REMEDY"
    }
    assert contract.get_case_rounds(args=[case_id]).call() == [record["id"]]
