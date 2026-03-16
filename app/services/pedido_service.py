from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas import schemas
from app.schemas.schemas import PedidoCreate, PedidoItemCreate
from app.models import models
from app.models.models import CanalPedido, StatusPedido
from app.services.pagamento_mock_service import PagamentoMockService

def validar_estoque(db: Session, itens: list):
    for item in itens:
        estoque = db.query(models.Estoque).filter(
            models.Estoque.produto_id == item.produto_id
        ).first()
        
        if not estoque or estoque.quantidade < item.quantidade:
            raise HTTPException(
                status_code=409,
                detail={
                    "error": "ESTOQUE_INSUFICIENTE",
                    "message": f"Estoque insuficiente para o produto {item.produto_id}",
                    "details": [{
                        "field": "quantidade",
                        "issue": f"Disponível: {estoque.quantidade if estoque else 0}, Solicitado: {item.quantidade}"
                    }]
                }
            )
    return True

def calcular_total(db: Session, itens: list):
    total = 0
    for item in itens:
        produto = db.query(models.Produto).filter(models.Produto.id == item.produto_id).first()
        if produto:
            total += produto.preco * item.quantidade
    return total

def criar_pedido(db: Session, pedido: schemas.PedidoCreate):
    validar_estoque(db, pedido.itens)
    
    valor_total = calcular_total(db, pedido.itens)
    
    db_pedido = models.Pedido(
        usuario_id=pedido.cliente_id,
        canal_pedido= CanalPedido(pedido.canal_pedido.value),
        valor_total=valor_total
    )
    db.add(db_pedido)
    db.flush()
    
    for item in pedido.itens:
        produto = db.query(models.Produto).filter(models.Produto.id == item.produto_id).first()
        db_item = models.ItemPedido(
            pedido_id=db_pedido.id,
            produto_id=item.produto_id,
            quantidade=item.quantidade,
            preco_unitario=produto.preco if produto else 0
        )
        db.add(db_item)
    
    # Registrar auditoria
    db.add(models.Auditoria(
        usuario_id=pedido.cliente_id,
        pedido_id=db_pedido.id,
        acao="CRIAR_PEDIDO"
    ))
    
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

async def processar_pagamento_mock(db: Session, pedido_id: int):
    pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    # Usar o serviço mock
    status_pag, transacao_id, detalhes = await PagamentoMockService.processar_pagamento(
        valor=pedido.valor_total
    )
    
    # Atualizar status do pedido baseado no pagamento
    if status_pag == "APROVADO":
        pedido.status = StatusPedido.PAGAMENTO_CONFIRMADO
        
        # Adicionar pontos de fidelidade (1 ponto a cada R$10)
        db.add(models.Fidelidade(
            cliente_id=pedido.usuario_id,
            pontos=int(pedido.valor_total / 10),
            tipo="ACUMULO",
            pedido_id=pedido_id
        ))
    elif status_pag == "RECUSADO":
        pedido.status = StatusPedido.CANCELADO
    
    
    # Registrar pagamento
    db_pagamento = models.Pagamento(
        pedido_id=pedido_id,
        valor=pedido.valor_total,
        metodo="MOCK",
        status=status_pag,
        transacao_id=transacao_id
    )
    db.add(db_pagamento)
    
    # Auditoria
    db.add(models.Auditoria(
        usuario_id=pedido.usuario_id,
        pedido_id=pedido_id,
        acao=f"PAGAMENTO_{status_pag}"
    ))
    
    db.commit()
    
    return {
        "pedido_id": pedido_id,
        "status": status_pag,
        "transacao_id": transacao_id
    }

def consultar_pontos(db: Session, cliente_id: int):
    pontos = db.query(models.Fidelidade).filter(
        models.Fidelidade.cliente_id == cliente_id,
        models.Fidelidade.tipo == "ACUMULO"
    ).all()
    
    total = sum(p.pontos for p in pontos)
    
    return {
        "cliente_id": cliente_id,
        "total_pontos": total
    }