# file_parser.py
from __future__ import annotations

from io import BytesIO
from typing import Any, Dict, List, Literal, Tuple

import pandas as pd


EXPECTED_COLUMNS = [
    "nombre_estudiante",
    "anio_inicio",
    "anio_fin",
    "promedio_graduacion",
    "promedio_actual",
    "centro_escolar",
    "NUE",
    "estado",
]


FileKind = Literal["csv", "xlsx"]


def read_students_file(content: bytes, kind: FileKind) -> Tuple[List[Dict[str, Any]], List[str]]:
   
    bio = BytesIO(content)

    if kind == "csv":
        df = pd.read_csv(bio, dtype=str, keep_default_na=False)  # todo string para controlar casting nosotros
    else:
        df = pd.read_excel(bio, dtype=str, keep_default_na=False)

    df.columns = [c.strip() for c in df.columns]

    missing = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    if missing:
        return ([], missing)

    df = df[EXPECTED_COLUMNS]

    rows = df.to_dict(orient="records")
    return (rows, [])
