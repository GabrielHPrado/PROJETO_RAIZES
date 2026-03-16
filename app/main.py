from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from app.core.database import engine
from app.models.models import Base
from app.routes import auth_routes, produtos_routes, pedidos_routes, pagamentos_routes, fidelidade_routes

app = FastAPI(
    title="API Raízes do Nordeste",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router)
app.include_router(produtos_routes.router)
app.include_router(pedidos_routes.router)
app.include_router(pagamentos_routes.router)
app.include_router(fidelidade_routes.router)


@app.get("/")
def root():
    return {
        "message": "API Raízes do Nordeste funcionando",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    try:
        from sqlalchemy import text

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            db_status = "ok"
    except Exception:
        db_status = "erro"

    return {
        "status": "online",
        "database": db_status,
        "timestamp": datetime.now().isoformat()
    }

@app.on_event("startup")
async def startup_event():
    print("API iniciada")
    print("Docs: http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    print("API encerrada")