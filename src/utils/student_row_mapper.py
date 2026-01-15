# src/utils/student_row_mapper.py
from __future__ import annotations

from datetime import date
from typing import Any, Dict

from src.schemas.student import StudentCreate
from src.utils.casting import to_float, to_int


def row_to_student(row: Dict[str, Any]) -> StudentCreate:
    mapped = dict(row)

    mapped["anio_inicio"] = to_int(mapped.get("anio_inicio"))

    mapped["anio_fin"] = to_int(mapped.get("anio_fin"))
    mapped["NUE"] = to_int(mapped.get("NUE"))

    mapped["promedio_actual"] = to_float(mapped.get("promedio_actual"))
    mapped["promedio_graduacion"] = to_float(mapped.get("promedio_graduacion"))

    mapped["nombre_estudiante"] = str(mapped.get("nombre_estudiante", "")).strip()
    mapped["centro_escolar"] = (
        None if mapped.get("centro_escolar") in (None, "") else str(mapped.get("centro_escolar")).strip()
    )

    mapped["estado"] = str(mapped.get("estado", "")).strip().lower()

    return StudentCreate.model_validate(mapped)
