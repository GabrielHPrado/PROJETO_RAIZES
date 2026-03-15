from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import pedido_service
# NÃO PRECISA DE models AQUI porque só usa o service

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])

@router.post("/processar/{pedido_id}")
def processar_pagamento(pedido_id: int, db: Session = Depends(get_db)):
    return pedido_service.processar_pagamento_mock(db, pedido_id)