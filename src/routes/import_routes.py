from __future__ import annotations

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status

from src.db.db import get_db
from src.repositories.student_repository import StudentRepository
from src.services.import_service import ImportService
from src.schemas.import_result import ImportResult

router = APIRouter(prefix="/import", tags=["Import"])


def get_import_service(db=Depends(get_db)) -> ImportService:
    repo = StudentRepository(db)
    return ImportService(repo)


@router.post("/students", response_model=ImportResult)
async def import_students(
    file: UploadFile = File(...),
    service: ImportService = Depends(get_import_service),
):
    filename = (file.filename or "").lower()

    if filename.endswith(".csv"):
        kind = "csv"
    elif filename.endswith(".xlsx"):
        kind = "xlsx"
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato inválido. Solo se permite .csv o .xlsx",
        )

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Archivo vacío")

    return await service.import_file(content=content, kind=kind, batch_size=1000)
