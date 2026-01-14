# src/utils/dedupe.py
from __future__ import annotations

from typing import List, Set, Tuple

from src.schemas.import_result import RowError
from src.schemas.student import StudentCreate


def validate_no_duplicates_in_file(
    students: List[StudentCreate],
    start_row: int = 1,
) -> Tuple[List[StudentCreate], List[RowError]]:
    """
    Valida duplicados dentro del archivo:
    - NUE duplicado
    - nombre_estudiante duplicado (case-insensitive, trimmed)
    Retorna (valid_students, errors)
    """
    seen_nue: Set[int] = set()
    seen_nombre: Set[str] = set()

    valid: List[StudentCreate] = []
    errors: List[RowError] = []

    for i, s in enumerate(students, start=start_row):
        if s.NUE in seen_nue:
            errors.append(
                RowError(row=i, field="NUE", value=s.NUE, message="NUE duplicado en el archivo")
            )
            continue
        seen_nue.add(s.NUE)

        nombre_key = s.nombre_estudiante.strip().lower()
        if nombre_key in seen_nombre:
            errors.append(
                RowError(
                    row=i,
                    field="nombre_estudiante",
                    value=s.nombre_estudiante,
                    message="nombre_estudiante duplicado en el archivo",
                )
            )
            continue
        seen_nombre.add(nombre_key)

        valid.append(s)

    return valid, errors
