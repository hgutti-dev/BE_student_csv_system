# BE CSV System (Backend)

Backend desarrollado con **Python**, **FastAPI** y **MongoDB**, diseñado para:

- **Procesar la carga de archivos** `.csv` y `.xlsx/.xlsm`
- **Validar datos** antes de su inserción
- **Insertar / actualizar registros** en MongoDB de forma eficiente
- **Exponer endpoints REST** para que el frontend consulte los datos almacenados

La arquitectura sigue **buenas prácticas**, aplicando **Service Layer + Repository Pattern** para mantener un código limpio, escalable y fácil de mantener.

---

## 🧩 Funcionalidades

- 📤 **Carga de archivos (CSV / Excel)**
  - Soporta `.csv`, `.xlsx`, `.xlsm`
  - Lectura eficiente por filas
  - Validación por campo antes de insertar
- ✅ **Validaciones de negocio**:
  - Campos requeridos
  - Tipos de datos correctos
  - `anio_inicio` **no puede ser mayor al año actual**
  - Campos únicos (ej: `NUE`, `nombre_estudiante`)
  - Reglas condicionales (ej: promedios al graduarse)
- 🔁 **Upsert por identificador** (ej: NUE)
- 📋 **Listado de registros**
- ⚡ **Inserción optimizada en batch**
- ❌ **Mensajes de error claros**, indicando:
  - Fila
  - Campo
  - Valor inválido
  - Motivo del error

---

## 🛠️ Tecnologías

- **Python 3.10+**
- **FastAPI**
- **Pydantic v2**
- **MongoDB**
- **Motor (async MongoDB driver)**
- **Uvicorn**
- **Pandas**

---

## 📦 Requisitos

- Python **3.10 o superior**
- MongoDB (local o remoto)
- `pip` o `pipenv` / `poetry`

---

## 🚀 Instalación y ejecución

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload


### 1) Clonar el repositorio

```bash
git clone <tu-repo-url>
cd BE_CSV_SYSTEM
```

## Note

NEcesitas crear archivo .env y agregar las variables

MONGO_URI=
DB_NAME=demo_db
