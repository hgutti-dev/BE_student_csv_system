from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.db.db import get_client, DB_NAME
from src.routes.import_routes import router as import_router
from src.routes.student_routes import router as student_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    client = await get_client()
    app.state.client = client
    app.state.db = client[DB_NAME]
    # Si necesitas inicializar índices, colas, etc., hazlo aquí
    yield
    # --- Shutdown ---
    # Cierra recursos aquí si aplica (ej., cerrar cliente de DB)
    # await app.state.client.close()  # depende de tu driver; ajusta según tu implementación

app = FastAPI(
    title="Technical TEST",
    lifespan=lifespan,
)

# Registra rutas
app.include_router(import_router)
app.include_router(student_router)

@app.get("/")
async def root():
    return {"ok": True, "msg": "Bienvenido a CSV API!!"}