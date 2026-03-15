from fastapi import FastAPI
from database import engine
from models import Base

from routes import auth_routes
from routes import produtos_routes
from routes import pedidos_routes

app = FastAPI(
    title="API Raízes do Nordeste",
    version="1.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router)
app.include_router(produtos_routes.router)
app.include_router(pedidos_routes.router)


@app.get("/")
def root():
    return {"message": "API funcionando"}