from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db 
from app.services import pedido_service

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])

@router.post("/processar/{pedido_id}")
async def processar_pagamento(pedido_id: int, db: Session = Depends(get_db)):
    return await pedido_service.processar_pagamento_mock(db, pedido_id)