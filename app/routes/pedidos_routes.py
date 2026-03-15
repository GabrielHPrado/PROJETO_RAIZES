from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, models  # <-- ADICIONEI O models AQUI
from app.services import pedido_service

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("/", response_model=schemas.PedidoResponse)
def criar_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    return pedido_service.criar_pedido(db, pedido)

@router.get("/")
def listar_pedidos(db: Session = Depends(get_db)):
    return db.query(models.Pedido).all()

@router.get("/{pedido_id}")
def buscar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido