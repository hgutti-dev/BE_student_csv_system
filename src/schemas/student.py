from __future__ import annotations

from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


EstadoEstudiante = Literal["activo", "graduado"]


class StudentBase(BaseModel):
    nombre_estudiante: str = Field(..., min_length=1)
    anio_inicio: int = Field(..., ge=1900)
    anio_fin: Optional[int] = Field(default=None, ge=1900)
    promedio_graduacion: Optional[float] = Field(default=None, ge=0, le=10)
    promedio_actual: Optional[float] = Field(default=None, ge=0, le=10)
    centro_escolar: Optional[str] = None
    NUE: int = Field(..., ge=1)
    estado: EstadoEstudiante

    @field_validator("nombre_estudiante")
    @classmethod
    def normalize_nombre(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("nombre_estudiante no puede estar vacío")
        return v

    @field_validator("anio_inicio", mode="before")
    @classmethod
    def validate_anio_inicio(cls, v):
        if v is None:
            raise ValueError("anio_inicio es requerido")

        try:
            v = int(str(v).strip())
        except Exception:
            raise ValueError("anio_inicio debe ser numérico")

        current_year = datetime.utcnow().year
        if v > current_year:
            raise ValueError(
                f"anio_inicio no puede ser mayor al año actual ({current_year})"
            )
        return v


    @model_validator(mode="after")
    def validate_graduado_promedios(self):
        if self.estado == "graduado":
            if self.promedio_actual is None or self.promedio_graduacion is None:
                raise ValueError("Si estado=graduado, promedio_actual y promedio_graduacion son requeridos")
            # Importante: comparación “igual” con floats (tolerancia mínima)
            if abs(self.promedio_actual - self.promedio_graduacion) > 1e-9:
                raise ValueError("Si estado=graduado, promedio_actual y promedio_graduacion deben ser iguales")
        return self


class StudentCreate(StudentBase):
    pass


class StudentRead(StudentBase):
    id: str = Field(..., description="ID único en MongoDB")
    model_config = ConfigDict(from_attributes=True)
