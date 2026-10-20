"""Explicit opt-in: real PoB2 container calculations, not mocked oracle results."""

import copy
import json
import os
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

import pytest

from exileai.pob.codec import decode_build_code
from exileai.pob.validation import active_import_nodes
from scripts.pob_spike import run_experiment

pytestmark = pytest.mark.skipif(
    os.environ.get("EXILEAI_POB_INTEGRATION") != "1",
    reason="Set EXILEAI_POB_INTEGRATION=1 to start pinned Docker workers",
)


def request() -> dict[str, Any]:
    root = Path(__file__).resolve().parents[2]
    result: dict[str, Any] = json.loads(
        (root / "tests/fixtures/spark-spike-request.json").read_text()
    )
    result["xml"] = decode_build_code(
        (root / "tests/fixtures/spark-diagnostic.pobcode").read_text()
    )
    return result


def test_fresh_workers_reproduce_budget_preserving_swap() -> None:
    root = Path(__file__).resolve().parents[2]
    expected = json.loads(
        (root / "tests/fixtures/spark-diagnostic.expected.json").read_text()
    )
    first = run_experiment(request())
    second = run_experiment(request())
    for result in (first, second):
        assert (
            result["before"]["points"]
            == result["after"]["points"]
            == [1, 0, 0, 0, 0, 0]
        )
        assert result["before"]["allocated"] == [4739, 54447]
        assert result["after"]["allocated"] == [44871, 54447]
        assert result["deltas"]["CombinedDPS"] < 0
        assert result["deltas"]["EnergyShield"] > 0
        assert result["after"]["metrics"]["Life"] == result["before"]["metrics"]["Life"]
        assert result["before"]["metric_states"] == {}
        assert result["original_xml"] == request()["xml"]
        assert result["objective"] == request()["objective"]
        for stage in ("before", "after"):
            assert result[stage]["metrics"] == pytest.approx(
                expected[stage]["metrics"], rel=1e-9, abs=1e-8
            )
    for stage in ("imported", "before", "after"):
        assert first[stage]["metrics"] == pytest.approx(
            second[stage]["metrics"], rel=1e-9, abs=1e-8
        )


@pytest.mark.parametrize(
    "action",
    [
        {"remove": -1, "add": 44871},
        {"remove": 54447, "add": 44871},
        {"remove": 4739, "add": 4739},
    ],
)
def test_invalid_swaps_are_rejected(action: dict[str, int]) -> None:
    value = copy.deepcopy(request())
    value["action"] = action
    with pytest.raises(RuntimeError, match="experiment failed"):
        run_experiment(value)


def test_missing_metric_is_not_silently_omitted() -> None:
    value = request()
    value["metrics"] = ["ThisMetricDoesNotExist"]
    with pytest.raises(RuntimeError, match="experiment failed"):
        run_experiment(value)


def test_contributed_build_import_is_explicitly_unverified() -> None:
    root = Path(__file__).resolve().parents[2] / "tests/fixtures"
    value = json.loads((root / "gemling-import-request.json").read_text())
    value["xml"] = decode_build_code(
        (root / "gemling-spark-contributed.pobcode").read_text()
    )
    result = run_experiment(value)
    assert result["benchmark_eligible"] is False
    assert result["assumption_policy"] == "as-imported-unverified"
    assert result["main_socket_group"] == 2
    assert result["allocation_reconciliation"]["exact_match"] is True
    assert result["imported"]["allocated"] == active_import_nodes(value["xml"])
    assert result["imported"]["points"] == [121, 8, 0, 6, 0, 0]
    assert len(result["imported"]["not_directly_connected"]) == 11
    assert result["imported"]["metrics"] == pytest.approx(
        {
            "CombinedDPS": 211277.80852331,
            "TotalDPS": 211277.80852331,
            "Life": 1554,
            "EnergyShield": 0,
            "TotalEHP": 11234.400170098,
            "PhysicalMaximumHitTaken": 7085,
            "FireMaximumHitTaken": 11427,
            "ColdMaximumHitTaken": 25304,
            "LightningMaximumHitTaken": 19681,
            "ChaosMaximumHitTaken": 5855,
            "FireResist": 41,
            "ColdResist": 75,
            "LightningResist": 67,
            "ChaosResist": -21,
        },
        rel=1e-9,
        abs=1e-8,
    )


def test_flameblast_import_reports_granted_sockets_and_requirement_deficit() -> None:
    fixtures = Path(__file__).resolve().parents[2] / "tests/fixtures"
    value: dict[str, Any] = json.loads(
        (fixtures / "gemling-import-request.json").read_text()
    )
    value["xml"] = decode_build_code(
        (fixtures / "gemling-flameblast-contributed.pobcode").read_text()
    )
    result = run_experiment(value)
    assert result["benchmark_eligible"] is False
    reconciliation = result["allocation_reconciliation"]
    assert reconciliation["missing"] == []
    assert {node["id"] for node in reconciliation["added"]} == {26178, 62152}
    assert all(node["free"] and node["granted"] for node in reconciliation["added"])
    assert result["imported"]["not_directly_connected"] == []
    assert result["imported"]["points"] == [146, 8, 0, 9, 24, 24]
    assert result["imported"]["requirements"]["Dex"] == {
        "available": 64,
        "required": 76,
        "deficit": 12,
    }
    assert result["imported"]["metrics"]["CombinedDPS"] == pytest.approx(
        15565539.904953
    )
    assert result["imported"]["metrics"]["TotalDPS"] == pytest.approx(180416.46381579)
    assert result["imported"]["metrics"]["Life"] == 3257


def monk_request() -> dict[str, Any]:
    fixtures = Path(__file__).resolve().parents[2] / "tests/fixtures"
    value: dict[str, Any] = json.loads(
        (fixtures / "gemling-import-request.json").read_text()
    )
    value["xml"] = decode_build_code(
        (fixtures / "monk-whirling-assault-contributed.pobcode").read_text()
    )
    return value


def test_chaos_immunity_is_explicit_standard_json_not_fake_finite_metric() -> None:
    result = run_experiment(monk_request())
    assert result["imported"]["metrics"]["ChaosMaximumHitTaken"] is None
    assert result["imported"]["metric_states"]["ChaosMaximumHitTaken"] == {
        "state": "immune",
        "reason": "ChaosInoculation",
    }
    assert result["imported"]["metrics"]["CombinedDPS"] == pytest.approx(
        878963.48805864
    )
    assert result["imported"]["points"] == [121, 8, 0, 4, 0, 0]
    json.dumps(result, allow_nan=False)


def test_real_boss_benchmark_swap_preserves_budget_and_fixed_mechanics() -> None:
    fixtures = Path(__file__).resolve().parents[2] / "tests/fixtures"
    value = json.loads((fixtures / "monk-boss-spike-request.json").read_text())
    value["xml"] = monk_request()["xml"]
    expected = json.loads((fixtures / "monk-boss-spike.expected.json").read_text())
    first = run_experiment(value)
    second = run_experiment(value)
    for result in (first, second):
        assert (
            result["before"]["points"]
            == result["after"]["points"]
            == [121, 8, 0, 4, 0, 0]
        )
        assert set(result["after"]["allocated"]) == (
            set(result["before"]["allocated"]) - {52399}
        ) | {9050}
        assert (
            result["before"]["not_directly_connected"]
            == result["after"]["not_directly_connected"]
            == []
        )
        assert all(x["deficit"] == 0 for x in result["after"]["requirements"].values())
        assert result["after"]["metrics"]["ChaosMaximumHitTaken"] is None
        assert result["deltas"]["ChaosMaximumHitTaken"] is None
        assert (
            result["delta_states"]["ChaosMaximumHitTaken"]["after"]["state"] == "immune"
        )
        assert result["assumption_audit"]["policy"] == "conservative-boss-conditions-v1"
        assert result["scenario"] == value["scenario"]
        assert result["objective"] == value["objective"]
        assert result["deltas"]["CombinedDPS"] != 0
        for stage in ("before", "after"):
            for key, metric in expected[stage].items():
                if metric is None:
                    assert result[stage]["metrics"][key] is None
                else:
                    assert result[stage]["metrics"][key] == pytest.approx(
                        metric, rel=1e-9, abs=1e-8
                    )
        for section in ("Build", "Skills", "Items", "Config"):
            before = ElementTree.fromstring(result["audited_xml"])
            after = ElementTree.fromstring(result["modified_xml"])
            before_section, after_section = before.find(section), after.find(section)
            assert before_section is not None and after_section is not None
            if section == "Build":
                # Child PlayerStat/MinionStat records are cached outputs, not inputs.
                assert before_section.attrib == after_section.attrib
            else:
                assert ElementTree.tostring(before_section) == ElementTree.tostring(
                    after_section
                )
        for name in ("conditionKilledRecently", "usePowerCharges"):
            assert result["resolved_config_inputs"][name] is False
        json.dumps(result, allow_nan=False)
    for stage in ("before", "after"):
        for key, metric in first[stage]["metrics"].items():
            if metric is not None:
                assert metric == pytest.approx(
                    second[stage]["metrics"][key], rel=1e-9, abs=1e-8
                )
