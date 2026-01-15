# src/utils/mongo_errors.py
from __future__ import annotations

from typing import List

from pymongo.errors import BulkWriteError

from src.schemas.import_result import RowError


def bulk_write_error_to_row_errors(
    bwe: BulkWriteError,
    chunk_start_index: int,
) -> List[RowError]:
   
    errors: List[RowError] = []
    write_errors = (bwe.details or {}).get("writeErrors", [])

    for we in write_errors:
        op_index = we.get("index") or 0
        code = we.get("code")
        errmsg = we.get("errmsg", "Bulk write error")

       
        row_global = chunk_start_index + op_index + 1

        errors.append(
            RowError(
                row=row_global,
                field="unique_index" if code == 11000 else "*",
                value=None,
                message=errmsg,
            )
        )

    return errors
