from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.db.db import get_client, DB_NAME
from src.routes.import_routes import router as import_router
from src.routes.student_routes import router as student_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = await get_client()
    app.state.client = client
    app.state.db = client[DB_NAME]
   
    yield
    

app = FastAPI(
    title="Technical TEST",
    lifespan=lifespan,
)

# Registra rutas
app.include_router(import_router)
app.include_router(student_router)

origins = [
    "http://127.0.0.1:5173",  
    "http://localhost:5173",
    "http://127.0.0.1:5500",  
    "http://localhost:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          
    allow_credentials=True,
    allow_methods=["*"],           
    allow_headers=["*"],            
    
)

@app.get("/")
async def root():
    return {"ok": True, "msg": "Bienvenido a CSV API!!"}