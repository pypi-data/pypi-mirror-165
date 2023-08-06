import pytest
from coiled.magic import create_specifier


@pytest.mark.parametrize(
    ["version", "to_filter", "expected_result", "expected_str"],
    [
        ("0.0.1", ["0.0.1", "0.0.2", "0.1.0", "1.0.0"], ["0.0.1", "0.0.2"], "~=0.0.1"),
        (
            "0.0.1.dev0",
            ["0.0.1", "0.0.1.dev0", "0.0.1.dev2" "0.0.0", "0.0.3"],
            ["0.0.1", "0.0.1.dev0", "0.0.3"],
            "~=0.0.1.dev0",
        ),
        (
            "2022.06.01",
            ["2022.06.01", "2022.06.02", "2022.07.01"],
            ["2022.06.01", "2022.06.02"],
            "~=2022.6.1",
        ),
        ("2022c", ["2022c", "2022b", "2022rc0", "2022"], ["2022c"], "==2022c"),
        ("2.2", ["2.2", "2.1", "3", "2"], ["2.2"], "==2.2"),
    ],
)
def test_specifier_normal_priority(version, to_filter, expected_result, expected_str):
    spec = create_specifier(version, priority=50)
    assert list([v for v in to_filter if v in spec]) == expected_result
    assert str(spec) == expected_str, f"{str(spec)} does not equal {expected_str}"


@pytest.mark.parametrize(
    ["version", "to_filter", "expected_result", "expected_str"],
    [
        ("0.0.1", ["0.0.1", "0.0.2", "0.1.0", "1.0.0"], ["0.0.1"], "==0.0.1"),
        (
            "0.0.1.dev0",
            ["0.0.1", "0.0.1.dev0", "0.0.1.dev2", "0.0.0", "0.0.3"],
            ["0.0.1.dev0"],
            "==0.0.1.dev0",
        ),
        (
            "2022.06.01",
            ["2022.06.01", "2022.06.02", "2022.07.01"],
            ["2022.06.01"],
            "==2022.6.1",
        ),
        ("2022c", ["2022c", "2022b", "2022rc0" "2022"], ["2022c"], "==2022c"),
        ("2.2", ["2.2", "2.1", "3", "2"], ["2.2"], "==2.2"),
    ],
)
def test_specifier_critical_priority(version, to_filter, expected_result, expected_str):
    spec = create_specifier(version, priority=100)
    assert list([v for v in to_filter if v in spec]) == expected_result
    assert str(spec) == expected_str, f"{str(spec)} does not equal {expected_str}"
