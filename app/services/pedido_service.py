from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app import models, schemas
from datetime import datetime
import random
import uuid

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
                    "message": f"Estoque insuficiente",
                    "details": [{
                        "field": "quantidade",
                        "issue": f"Disponível: {estoque.quantidade if estoque else 0}"
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
        canal_pedido=pedido.canal_pedido.value,
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
    
    db.add(models.Auditoria(
        usuario_id=pedido.cliente_id,
        pedido_id=db_pedido.id,
        acao="CRIAR_PEDIDO"
    ))
    
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

def processar_pagamento_mock(db: Session, pedido_id: int):
    pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    rand = random.random()
    if rand < 0.7:
        status_pag = "APROVADO"
        pedido.status = models.StatusPedido.PAGAMENTO_CONFIRMADO
        
        db.add(models.Fidelidade(
            cliente_id=pedido.usuario_id,
            pontos=int(pedido.valor_total / 10),
            tipo="ACUMULO",
            pedido_id=pedido_id
        ))
    elif rand < 0.9:
        status_pag = "RECUSADO"
        pedido.status = models.StatusPedido.CANCELADO
    else:
        status_pag = "ERRO"
    
    transacao_id = f"MOCK_{uuid.uuid4().hex[:8].upper()}"
    
    db_pagamento = models.Pagamento(
        pedido_id=pedido_id,
        valor=pedido.valor_total,
        metodo="MOCK",
        status=status_pag,
        transacao_id=transacao_id
    )
    db.add(db_pagamento)
    
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