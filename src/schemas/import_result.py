from __future__ import annotations

from typing import Any, List, Optional
from pydantic import BaseModel


class RowError(BaseModel):
    row: int                 # fila 1-based como lo ve el usuario (incluye header? -> aquí lo manejamos como “fila de datos”)
    field: str
    value: Optional[Any] = None
    message: str


class ImportResult(BaseModel):
    total_rows: int
    inserted: int
    updated: int
    failed: int
    errors: List[RowError] = []
