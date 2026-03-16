from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.schemas import ProdutoCreate, ProdutoResponse, ErrorResponse
from app.models import models
from app.core.auth_deps import get_usuario_atual, requer_gerente_ou_admin, requer_admin  # IMPORTE TODAS AS FUNÇÕES

router = APIRouter(prefix="/produtos", tags=["Produtos"])

# GET /produtos - Listar com paginação (NÃO USA response_model=list)
@router.get("/")
def listar_produtos(
    page: int = Query(1, ge=1, description="Número da página"),
    limit: int = Query(10, ge=1, le=100, description="Itens por página"),
    db: Session = Depends(get_db),
    usuario_atual: models.Usuario = Depends(get_usuario_atual)  # Apenas autenticado
):
    """
    Lista todos os produtos com paginação
    """
    # Calcula offset
    skip = (page - 1) * limit
    
    # Busca produtos com paginação
    produtos = db.query(models.Produto).offset(skip).limit(limit).all()
    
    # Total de produtos
    total = db.query(models.Produto).count()
    
    # Calcula total de páginas
    pages = (total + limit - 1) // limit if total > 0 else 0
    
    return {
        "data": produtos,
        "page": page,
        "limit": limit,
        "total": total,
        "pages": pages
    }

# Versão alternativa que retorna lista (sem paginação)
@router.get("/todos", response_model=List[ProdutoResponse])
def listar_todos_produtos(
    db: Session = Depends(get_db),
    usuario_atual: models.Usuario = Depends(get_usuario_atual)
):
    """
    Lista todos os produtos (sem paginação)
    """
    return db.query(models.Produto).all()

# POST /produtos - Criar produto (apenas ADMIN ou GERENTE)
@router.post("/", response_model=ProdutoResponse, status_code=201)
def criar_produto(
    produto: ProdutoCreate,
    db: Session = Depends(get_db),
    usuario_atual: models.Usuario = Depends(requer_gerente_ou_admin)  # ADMIN ou GERENTE
):
    """
    Cria um novo produto (apenas ADMIN ou GERENTE)
    """
    # Verificar se já existe produto com mesmo nome
    produto_existente = db.query(models.Produto).filter(
        models.Produto.nome == produto.nome
    ).first()
    
    if produto_existente:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "PRODUTO_DUPLICADO",
                "message": f"Produto com nome '{produto.nome}' já existe"
            }
        )
    
    # Criar produto
    db_produto = models.Produto(
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco,
        ativo=True
    )
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    
    # Criar estoque inicial para o produto
    estoque = models.Estoque(
        produto_id=db_produto.id,
        quantidade=0,
        quantidade_minima=5
    )
    db.add(estoque)
    db.commit()
    
    # Registrar auditoria
    auditoria = models.Auditoria(
        usuario_id=usuario_atual.id,
        acao="CRIAR_PRODUTO",
        entidade="PRODUTO",
        entidade_id=db_produto.id,
        dados_novos=f"{db_produto.nome} - R${db_produto.preco}"
    )
    db.add(auditoria)
    db.commit()
    
    return db_produto

# GET /produtos/{produto_id} - Buscar por ID
@router.get("/{produto_id}", response_model=ProdutoResponse)
def buscar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario_atual: models.Usuario = Depends(get_usuario_atual)
):
    """
    Busca um produto pelo ID
    """
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    
    if not produto:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "PRODUTO_NAO_ENCONTRADO",
                "message": f"Produto com ID {produto_id} não encontrado"
            }
        )
    
    return produto

# PUT /produtos/{produto_id} - Atualizar produto
@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(
    produto_id: int,
    produto: ProdutoCreate,
    db: Session = Depends(get_db),
    usuario_atual: models.Usuario = Depends(requer_gerente_ou_admin)  # ADMIN ou GERENTE
):
    """
    Atualiza um produto existente (apenas ADMIN ou GERENTE)
    """
    db_produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    
    if not db_produto:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "PRODUTO_NAO_ENCONTRADO",
                "message": f"Produto com ID {produto_id} não encontrado"
            }
        )
    
    # Guardar dados antigos para auditoria
    dados_anteriores = f"{db_produto.nome} - R${db_produto.preco}"
    
    # Atualizar dados
    db_produto.nome = produto.nome
    db_produto.descricao = produto.descricao
    db_produto.preco = produto.preco
    
    db.commit()
    db.refresh(db_produto)
    
    # Registrar auditoria
    auditoria = models.Auditoria(
        usuario_id=usuario_atual.id,
        acao="ATUALIZAR_PRODUTO",
        entidade="PRODUTO",
        entidade_id=produto_id,
        dados_anteriores=dados_anteriores,
        dados_novos=f"{db_produto.nome} - R${db_produto.preco}"
    )
    db.add(auditoria)
    db.commit()
    
    return db_produto

# DELETE /produtos/{produto_id} - Deletar produto (apenas ADMIN)
@router.delete("/{produto_id}", status_code=204)
def deletar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario_atual: models.Usuario = Depends(requer_admin)  # Apenas ADMIN
):
    """
    Remove um produto (apenas ADMIN)
    """
    db_produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    
    if not db_produto:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "PRODUTO_NAO_ENCONTRADO",
                "message": f"Produto com ID {produto_id} não encontrado"
            }
        )
    
    # Registrar auditoria antes de deletar
    auditoria = models.Auditoria(
        usuario_id=usuario_atual.id,
        acao="DELETAR_PRODUTO",
        entidade="PRODUTO",
        entidade_id=produto_id,
        dados_anteriores=f"{db_produto.nome} - R${db_produto.preco}"
    )
    db.add(auditoria)
    
    # Deletar (ou desativar)
    db.delete(db_produto)
    db.commit()
    
    return None