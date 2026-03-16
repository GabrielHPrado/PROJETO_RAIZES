from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models import models
from app.schemas import schemas
from app.schemas.schemas import CanalPedidoEnum
from app.services import pedido_service
from app.core.auth_deps import get_usuario_atual

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post("/", response_model=schemas.PedidoResponse)
async def criar_pedido(
    pedido: schemas.PedidoCreate,
    db: Session = Depends(get_db),
    usuario_atual: models.Usuario = Depends(get_usuario_atual)
):

  
    if usuario_atual.perfil.value == "CLIENTE" and pedido.cliente_id != usuario_atual.id:
        raise HTTPException(
            status_code=403,
            detail="Você só pode criar pedidos para si mesmo"
        )

    return pedido_service.criar_pedido(db, pedido)


@router.get("/")
def listar_pedidos(
    canal_pedido: Optional[CanalPedidoEnum] = Query(None),
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    usuario_atual: models.Usuario = Depends(get_usuario_atual)
):

    query = db.query(models.Pedido)

  
    if usuario_atual.perfil.value == "CLIENTE":
        query = query.filter(models.Pedido.usuario_id == usuario_atual.id)

    if canal_pedido:
        query = query.filter(models.Pedido.canal_pedido == canal_pedido.value)

    if status:
        query = query.filter(models.Pedido.status == status)

    total = query.count()

    skip = (page - 1) * limit

    pedidos = (
        query.order_by(models.Pedido.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "data": pedidos,
        "page": page,
        "limit": limit,
        "total": total,
        "pages": (total + limit - 1) // limit
    }


@router.get("/{pedido_id}")
def buscar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario_atual: models.Usuario = Depends(get_usuario_atual)
):

    pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    
    if usuario_atual.perfil.value == "CLIENTE" and pedido.usuario_id != usuario_atual.id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    return pedido