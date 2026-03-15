from fastapi import FastAPI
from app.models import Base, engine
from app.routes import auth_routes, produtos_routes, pedidos_routes, pagamentos_routes, fidelidade_routes

app = FastAPI(
    title="API Raízes do Nordeste",
    version="1.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router)
app.include_router(produtos_routes.router)
app.include_router(pedidos_routes.router)
app.include_router(pagamentos_routes.router)
app.include_router(fidelidade_routes.router)

@app.get("/")
def root():
    return {"message": "API Raízes do Nordeste funcionando"}