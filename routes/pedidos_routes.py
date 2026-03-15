from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Pedido, ItemPedido
from schemas import PedidoCreate

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def criar_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):

    novo_pedido = Pedido(
        cliente_id=pedido.cliente_id,
        status="CRIADO"
    )

    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)

    for item in pedido.itens:

        novo_item = ItemPedido(
            pedido_id=novo_pedido.id,
            produto_id=item.produto_id,
            quantidade=item.quantidade
        )

        db.add(novo_item)

    db.commit()

    return {"pedido_id": novo_pedido.id}


@router.get("/")
def listar_pedidos(db: Session = Depends(get_db)):

    pedidos = db.query(Pedido).all()

    return pedidos


@router.patch("/{pedido_id}/status")
def atualizar_status(pedido_id: int, status: str, db: Session = Depends(get_db)):

    pedido = db.query(Pedido).filter(
        Pedido.id == pedido_id
    ).first()

    pedido.status = status

    db.commit()

    return {"msg": "status atualizado"}