from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Produto
from schemas import ProdutoCreate

router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):

    novo = Produto(
        nome=produto.nome,
        preco=produto.preco
    )

    db.add(novo)
    db.commit()

    return novo


@router.get("/")
def listar_produtos(db: Session = Depends(get_db)):

    return db.query(Produto).all()