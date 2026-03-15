import random
import uuid
from datetime import datetime
from typing import Dict, Tuple

class PagamentoMockService:
    """
    SIMULAÇÃO de gateway de pagamento externo
    """
    
    @staticmethod
    async def processar_pagamento(valor: float, metodo: str = "MOCK") -> Tuple[str, str, Dict]:
        """
        Retorna: (status, transacao_id, detalhes)
        Status possíveis: APROVADO, RECUSADO, ERRO
        """
        # Simula latência de rede
        import asyncio
        await asyncio.sleep(1)
        
        # Gera ID único
        transacao_id = f"MOCK_{uuid.uuid4().hex[:8].upper()}"
        
        # Regras de simulação:
        # - 70% chance de aprovação
        # - 20% chance de recusa
        # - 10% chance de erro
        
        rand = random.random()
        
        if rand < 0.7:  # 70% aprovado
            status = "APROVADO"
            motivo = "Transação aprovada"
        elif rand < 0.9:  # 20% recusado
            status = "RECUSADO"
            motivo = "Cartão recusado"
        else:  # 10% erro
            status = "ERRO"
            motivo = "Erro de comunicação com o provedor"
        
        detalhes = {
            "transacao_id": transacao_id,
            "status": status,
            "motivo": motivo,
            "processado_em": datetime.now().isoformat(),
            "valor": valor
        }
        
        return status, transacao_id, detalhes