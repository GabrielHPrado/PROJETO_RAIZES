
from fastapi import FastAPI
from app.core.database import engine
from app.models.models import Base
from app.routes import auth_routes, produtos_routes, pedidos_routes, pagamentos_routes, fidelidade_routes

app = FastAPI(
    title="API Raízes do Nordeste",
    version="1.0"
)

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Incluir as rotas
app.include_router(auth_routes.router)
app.include_router(produtos_routes.router)
app.include_router(pedidos_routes.router)
app.include_router(pagamentos_routes.router)
app.include_router(fidelidade_routes.router)

@app.get("/")
def root():
    return {"message": "API Raízes do Nordeste funcionando"}