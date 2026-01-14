# src/services/import_service.py
from __future__ import annotations

from typing import  List

from fastapi import HTTPException, status
from pymongo.errors import BulkWriteError

from src.repositories.student_repository import StudentRepository
from src.schemas.import_result import ImportResult, RowError
from src.schemas.student import StudentCreate
from src.utils.file_parsers import read_students_file, FileKind

from src.utils.student_row_mapper import row_to_student
from src.utils.dedupe import validate_no_duplicates_in_file
from src.utils.iterables import chunked
from src.utils.mongo_errors import bulk_write_error_to_row_errors


class ImportService:
    def __init__(self, repo: StudentRepository) -> None:
        self._repo = repo

    async def import_file(self, content: bytes, kind: FileKind, batch_size: int = 1000) -> ImportResult:
        rows, missing = read_students_file(content, kind)
        if missing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Columnas faltantes: {missing}",
            )

        total = len(rows)
        errors: List[RowError] = []

        # 1) Mapear filas -> Students (capturando errores por fila)
        students: List[StudentCreate] = []
        for idx, r in enumerate(rows, start=1):
            try:
                students.append(row_to_student(r))
            except Exception as e:
                errors.append(RowError(row=idx, field="*", value=r, message=str(e)))

        # 2) Duplicados dentro del archivo
        valid_students, dup_errors = validate_no_duplicates_in_file(students, start_row=1)
        errors.extend(dup_errors)

        inserted = 0
        updated = 0

        # 3) Persistencia por chunks
        for start_index, chunk in chunked(valid_students, batch_size):
            try:
                ins, upd = await self._repo.bulk_upsert_by_NUE(chunk)
                inserted += ins
                updated += upd
            except BulkWriteError as bwe:
                errors.extend(bulk_write_error_to_row_errors(bwe, chunk_start_index=start_index))
                continue

        return ImportResult(
            total_rows=total,
            inserted=inserted,
            updated=updated,
            failed=len(errors),
            errors=errors,
        )
