from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db  
from app.services import pedido_service

router = APIRouter(prefix="/fidelidade", tags=["Fidelidade"])

@router.get("/pontos/{cliente_id}")
def consultar_pontos(cliente_id: int, db: Session = Depends(get_db)):
    return pedido_service.consultar_pontos(db, cliente_id)