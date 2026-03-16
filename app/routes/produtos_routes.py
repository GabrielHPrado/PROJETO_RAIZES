from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.schemas import ProdutoCreate, ProdutoResponse
from app.models import models
from app.core.auth_deps import get_usuario_atual, requer_gerente_ou_admin, requer_admin

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.get("/")
def listar_produtos(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    usuario_atual: models.Usuario = Depends(get_usuario_atual)
):
   
    skip = (page - 1) * limit

    produtos = db.query(models.Produto).offset(skip).limit(limit).all()
    total = db.query(models.Produto).count()

    pages = (total + limit - 1) // limit if total > 0 else 0

    return {
        "data": produtos,
        "page": page,
        "limit": limit,
        "total": total,
        "pages": pages
    }


@router.get("/todos", response_model=List[ProdutoResponse])
def listar_todos_produtos(
    db: Session = Depends(get_db),
    usuario_atual: models.Usuario = Depends(get_usuario_atual)
):
    return db.query(models.Produto).all()


@router.post("/", response_model=ProdutoResponse, status_code=201)
def criar_produto(
    produto: ProdutoCreate,
    db: Session = Depends(get_db),
    usuario_atual: models.Usuario = Depends(requer_gerente_ou_admin)
):
    
    produto_existente = db.query(models.Produto).filter(
        models.Produto.nome == produto.nome
    ).first()

    if produto_existente:
        raise HTTPException(
            status_code=400,
            detail="Produto com esse nome já existe"
        )

    novo_produto = models.Produto(
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco,
        ativo=True
    )

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

   
    estoque = models.Estoque(
        produto_id=novo_produto.id,
        quantidade=0,
        quantidade_minima=5
    )

    db.add(estoque)
    db.commit()

    
    auditoria = models.Auditoria(
        usuario_id=usuario_atual.id,
        acao="CRIAR_PRODUTO",
        entidade="PRODUTO",
        entidade_id=novo_produto.id
    )

    db.add(auditoria)
    db.commit()

    return novo_produto


@router.get("/{produto_id}", response_model=ProdutoResponse)
def buscar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario_atual: models.Usuario = Depends(get_usuario_atual)
):
    produto = db.query(models.Produto).filter(
        models.Produto.id == produto_id
    ).first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return produto


@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(
    produto_id: int,
    produto: ProdutoCreate,
    db: Session = Depends(get_db),
    usuario_atual: models.Usuario = Depends(requer_gerente_ou_admin)
):
    db_produto = db.query(models.Produto).filter(
        models.Produto.id == produto_id
    ).first()

    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    db_produto.nome = produto.nome
    db_produto.descricao = produto.descricao
    db_produto.preco = produto.preco

    db.commit()
    db.refresh(db_produto)

    auditoria = models.Auditoria(
        usuario_id=usuario_atual.id,
        acao="ATUALIZAR_PRODUTO",
        entidade="PRODUTO",
        entidade_id=produto_id
    )

    db.add(auditoria)
    db.commit()

    return db_produto


@router.delete("/{produto_id}", status_code=204)
def deletar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario_atual: models.Usuario = Depends(requer_admin)
):
    produto = db.query(models.Produto).filter(
        models.Produto.id == produto_id
    ).first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    auditoria = models.Auditoria(
        usuario_id=usuario_atual.id,
        acao="DELETAR_PRODUTO",
        entidade="PRODUTO",
        entidade_id=produto_id
    )

    db.add(auditoria)

    db.delete(produto)
    db.commit()

    return None