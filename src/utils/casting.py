# src/utils/casting.py
from __future__ import annotations

from typing import Any, Optional


def to_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    s = str(value).strip()
    if s == "":
        return None
    if not s.isdigit():
        raise ValueError("Debe ser numérico")
    return int(s)


def to_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    s = str(value).strip()
    if s == "":
        return None
    s = s.replace(",", ".")
    return float(s)
