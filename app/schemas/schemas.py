from pydantic import BaseModel, Field, validator, EmailStr
from typing import List, Optional
from enum import Enum
from datetime import datetime

# USUÁRIOS
class CanalPedidoEnum(str, Enum):
    APP = "APP"
    TOTEM = "TOTEM"
    BALCAO = "BALCAO"
    PICKUP = "PICKUP"
    WEB = "WEB"

class StatusPedidoEnum(str, Enum):
    AGUARDANDO_PAGAMENTO = "AGUARDANDO_PAGAMENTO"
    PAGAMENTO_CONFIRMADO = "PAGAMENTO_CONFIRMADO"
    EM_PREPARO = "EM_PREPARO"
    PRONTO = "PRONTO"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"

class PerfilEnum(str, Enum):
    ADMIN = "ADMIN"
    GERENTE = "GERENTE"
    ATENDENTE = "ATENDENTE"
    CLIENTE = "CLIENTE"

class TipoFidelidadeEnum(str, Enum):
    ACUMULO = "ACUMULO"
    RESGATE = "RESGATE"
    BONUS = "BONUS"

class MetodoPagamentoEnum(str, Enum):
    MOCK = "MOCK"
    CARTAO_CREDITO = "CARTAO_CREDITO"
    CARTAO_DEBITO = "CARTAO_DEBITO"
    PIX = "PIX"
    DINHEIRO = "DINHEIRO"

# USUÁRIOS
class UsuarioBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    email: EmailStr = Field(...)
    perfil: PerfilEnum = Field(default=PerfilEnum.CLIENTE)
    consentimento_lgpd: bool = Field(False)

class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., min_length=6, max_length=50)
    
    @validator('senha')
    def validar_senha(cls, v):
        if len(v) < 6:
            raise ValueError('Senha deve ter pelo menos 6 caracteres')
        if len(v) > 50:
            raise ValueError('Senha muito longa (máximo 50 caracteres)')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "nome": "Gabriel Henrique",
                "email": "gabriel@email.com",
                "senha": "123456",
                "perfil": "CLIENTE",
                "consentimento_lgpd": True
            }
        }

class UsuarioLogin(BaseModel):
    email: EmailStr = Field(...)
    senha: str = Field(...)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "gabriel@email.com",
                "senha": "123456"
            }
        }

class UsuarioResponse(UsuarioBase):
    id: int
    data_consentimento: Optional[datetime] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "nome": "Gabriel Henrique",
                "email": "gabriel@email.com",
                "perfil": "CLIENTE",
                "consentimento_lgpd": True,
                "data_consentimento": "2026-03-16T10:30:00",
                "created_at": "2026-03-16T10:30:00"
            }
        }

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponse
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "usuario": {
                    "id": 1,
                    "nome": "Gabriel Henrique",
                    "email": "gabriel@email.com",
                    "perfil": "CLIENTE"
                }
            }
        }

# PRODUTOS
class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    descricao: Optional[str] = Field(None, max_length=500)
    preco: float = Field(..., gt=0)

class ProdutoCreate(ProdutoBase):
    pass
    
    class Config:
        json_schema_extra = {
            "example": {
                "nome": "Baião de Dois",
                "descricao": "Arroz, feijão verde, queijo coalho e temperos",
                "preco": 32.90
            }
        }

class ProdutoResponse(ProdutoBase):
    id: int
    ativo: bool = True
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# ESTOQUE
class EstoqueBase(BaseModel):
    produto_id: int
    quantidade: int = Field(..., ge=0)
    quantidade_minima: int = Field(5, ge=0)

class EstoqueCreate(EstoqueBase):
    pass

class EstoqueResponse(EstoqueBase):
    id: int
    unidade_id: int = 1
    
    class Config:
        from_attributes = True

class EstoqueMovimentacao(BaseModel):
    produto_id: int
    quantidade: int = Field(...)
    
    class Config:
        json_schema_extra = {
            "example": {
                "produto_id": 1,
                "quantidade": -2
            }
        }

# PEDIDOS
class PedidoItemBase(BaseModel):
    produto_id: int
    quantidade: int = Field(..., gt=0)

class PedidoItemCreate(PedidoItemBase):
    pass
    
    class Config:
        json_schema_extra = {
            "example": {
                "produto_id": 1,
                "quantidade": 2
            }
        }

class PedidoItemResponse(PedidoItemBase):
    id: int
    pedido_id: int
    preco_unitario: float
    subtotal: float
    
    class Config:
        from_attributes = True

class PedidoCreate(BaseModel):
    cliente_id: int = Field(...)
    canal_pedido: CanalPedidoEnum = Field(...)
    itens: List[PedidoItemCreate] = Field(..., min_items=1)
    observacoes: Optional[str] = Field(None, max_length=500)
    
    @validator('itens')
    def validar_itens_duplicados(cls, v):
        produtos = [item.produto_id for item in v]
        if len(produtos) != len(set(produtos)):
            raise ValueError('Não é permitido produtos duplicados no pedido')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "cliente_id": 1,
                "canal_pedido": "APP",
                "itens": [
                    {"produto_id": 1, "quantidade": 2},
                    {"produto_id": 2, "quantidade": 1}
                ],
                "observacoes": "Sem cebola, por favor"
            }
        }

class PedidoResponse(BaseModel):
    id: int
    usuario_id: int
    canal_pedido: str
    status: str
    valor_total: float
    observacoes: Optional[str] = None
    created_at: datetime
    itens: Optional[List[PedidoItemResponse]] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "usuario_id": 1,
                "canal_pedido": "APP",
                "status": "AGUARDANDO_PAGAMENTO",
                "valor_total": 65.80,
                "observacoes": "Sem cebola",
                "created_at": "2026-03-16T10:30:00"
            }
        }

class PedidoListResponse(BaseModel):
    data: List[PedidoResponse]
    page: int
    limit: int
    total: int
    pages: int
    filtros: Optional[dict] = None

# PAGAMENTOS
class PagamentoRequest(BaseModel):
    pedido_id: int
    metodo: MetodoPagamentoEnum = MetodoPagamentoEnum.MOCK
    detalhes: Optional[dict] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "pedido_id": 1,
                "metodo": "MOCK"
            }
        }

class PagamentoResponse(BaseModel):
    pedido_id: int
    status: str
    transacao_id: Optional[str] = None
    mensagem: Optional[str] = None
    processado_em: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "pedido_id": 1,
                "status": "APROVADO",
                "transacao_id": "MOCK_ABC123",
                "mensagem": "Transação aprovada",
                "processado_em": "2026-03-16T10:31:00"
            }
        }

# FIDELIDADE
class FidelidadeBase(BaseModel):
    cliente_id: int
    pontos: int = Field(..., ge=0)
    tipo: TipoFidelidadeEnum
    pedido_id: Optional[int] = None
    descricao: Optional[str] = None

class FidelidadeCreate(FidelidadeBase):
    pass

class FidelidadeResponse(FidelidadeBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PontosResponse(BaseModel):
    cliente_id: int
    total_pontos: int
    historico: Optional[List[FidelidadeResponse]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "cliente_id": 1,
                "total_pontos": 150
            }
        }

# AUDITORIA
class AuditoriaResponse(BaseModel):
    id: int
    usuario_id: Optional[int] = None
    pedido_id: Optional[int] = None
    acao: str
    entidade: Optional[str] = None
    entidade_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# ERROS
class ErrorDetail(BaseModel):
    field: Optional[str] = None
    issue: str

class ErrorResponse(BaseModel):
    error: str
    message: str
    status_code: Optional[int] = None
    timestamp: Optional[str] = None
    path: Optional[str] = None
    method: Optional[str] = None
    details: Optional[List[ErrorDetail]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "ESTOQUE_INSUFICIENTE",
                "message": "Não há quantidade suficiente para um ou mais itens",
                "status_code": 409,
                "timestamp": "2026-03-16T10:30:00",
                "path": "/pedidos",
                "method": "POST",
                "details": [
                    {
                        "field": "itens[0].quantidade",
                        "issue": "Disponível: 1, Solicitado: 2"
                    }
                ]
            }
        }

# HEALTH CHECK
class HealthResponse(BaseModel):
    status: str
    timestamp: str
    database: str
    version: str