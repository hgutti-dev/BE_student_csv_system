from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple
from bson import ObjectId
from pymongo import UpdateOne
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

from src.schemas.student import StudentCreate, StudentRead


class StudentRepository:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._collection: AsyncIOMotorCollection = db["students"]

    async def ensure_indexes(self) -> None:
        # Unicidad real en BD
        await self._collection.create_index("nombre_estudiante", unique=True)
        await self._collection.create_index("NUE", unique=True)

    @staticmethod
    def _doc_to_read(doc: Dict[str, Any]) -> StudentRead:
        return StudentRead(
            id=str(doc["_id"]),
            nombre_estudiante=doc["nombre_estudiante"],
            anio_inicio=doc["anio_inicio"],
            anio_fin=doc.get("anio_fin"),
            promedio_graduacion=doc.get("promedio_graduacion"),
            promedio_actual=doc.get("promedio_actual"),
            centro_escolar=doc.get("centro_escolar"),
            NUE=doc["NUE"],
            estado=doc["estado"],
        )

    async def get_by_id(self, student_id: str) -> Optional[StudentRead]:
        if not ObjectId.is_valid(student_id):
            return None
        doc = await self._collection.find_one({"_id": ObjectId(student_id)})
        return self._doc_to_read(doc) if doc else None

    async def list(self, limit: int = 50, skip: int = 0) -> List[StudentRead]:
        cursor = self._collection.find({}).skip(skip).limit(limit).sort("nombre_estudiante", 1)
        docs = await cursor.to_list(length=limit)
        return [self._doc_to_read(d) for d in docs]

    async def bulk_upsert_by_NUE(
        self,
        students: List[StudentCreate],
    ) -> Tuple[int, int]:
        """
        Upsert por NUE: si existe, actualiza; si no, inserta.
        Retorna (inserted, updated).
        """
        if not students:
            return (0, 0)

        ops: List[UpdateOne] = []
        for s in students:
            doc = s.model_dump()
            ops.append(
                UpdateOne(
                    {"NUE": doc["NUE"]},
                    {"$set": doc},
                    upsert=True,
                )
            )

        # ordered=False => continúa aunque una operación falle (mejor para batch grandes)
        res = await self._collection.bulk_write(ops, ordered=False)
        inserted = res.upserted_count
        updated = res.modified_count
        return inserted, updated
