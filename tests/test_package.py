"""Verify the installed package resolves to this source checkout."""

from pathlib import Path

import exileai


def test_installed_package_is_local() -> None:
    assert exileai.__file__ is not None
    expected = Path(__file__).resolve().parents[1] / "src" / "exileai" / "__init__.py"
    assert Path(exileai.__file__).resolve() == expected
