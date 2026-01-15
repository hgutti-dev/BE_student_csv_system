from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from src.db.db import get_db
from src.repositories.student_repository import StudentRepository
from src.schemas.student import StudentRead

router = APIRouter(prefix="/students", tags=["Students"])


def get_repo(db=Depends(get_db)) -> StudentRepository:
    return StudentRepository(db)


@router.get("", response_model=list[StudentRead])
async def list_students(
    limit: int = Query(50, ge=1, le=200),
    skip: int = Query(0, ge=0),
    repo: StudentRepository = Depends(get_repo),
):
    return await repo.list(limit=limit, skip=skip)


