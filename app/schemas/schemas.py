from pydantic import BaseModel, validator
from typing import List, Optional
from enum import Enum

class CanalPedidoEnum(str, Enum):
    APP = "APP"
    TOTEM = "TOTEM"
    BALCAO = "BALCAO"
    PICKUP = "PICKUP"
    WEB = "WEB"

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str
    consentimento_lgpd: bool = False
    
    class Config:
        json_schema_extra = {
            "example": {
                "nome": "Gabriel",
                "email": "test@gmail.com",
                "senha": "123teste",
                "consentimento_lgpd": True
            }
        }

class UsuarioLogin(BaseModel):
    email: str
    senha: str

class ProdutoCreate(BaseModel):
    nome: str
    descricao: str
    preco: float

class ProdutoResponse(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: float
    
    class Config:
        from_attributes = True

class PedidoItem(BaseModel):
    produto_id: int
    quantidade: int

class PedidoCreate(BaseModel):
    cliente_id: int
    canal_pedido: CanalPedidoEnum
    itens: List[PedidoItem]

class PedidoResponse(BaseModel):
    id: int
    cliente_id: int
    canal_pedido: str
    status: str
    valor_total: float
    
    class Config:
        from_attributes = True

class PagamentoRequest(BaseModel):
    pedido_id: int
    metodo: str = "MOCK"

class PagamentoResponse(BaseModel):
    pedido_id: int
    status: str
    transacao_id: Optional[str]

class PontosResponse(BaseModel):
    cliente_id: int
    total_pontos: int

class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[List[dict]] = None