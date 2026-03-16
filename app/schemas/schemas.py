from pydantic import BaseModel, Field, validator, EmailStr
from typing import List, Optional
from enum import Enum
from datetime import datetime


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


class UsuarioBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    perfil: PerfilEnum = PerfilEnum.CLIENTE
    consentimento_lgpd: bool = False


class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., min_length=6, max_length=50)

    @validator("senha")
    def validar_senha(cls, v):
        if len(v) < 6:
            raise ValueError("Senha deve ter pelo menos 6 caracteres")
        if len(v) > 50:
            raise ValueError("Senha muito longa (50 caracteres)")
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
    email: EmailStr
    senha: str


class UsuarioResponse(UsuarioBase):
    id: int
    data_consentimento: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponse


class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    descricao: Optional[str] = None
    preco: float = Field(..., gt=0)


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoResponse(ProdutoBase):
    id: int
    ativo: bool = True
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


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
    quantidade: int

    class Config:
        json_schema_extra = {
            "example": {
                "produto_id": 1,
                "quantidade": -2
            }
        }


class PedidoItemBase(BaseModel):
    produto_id: int
    quantidade: int = Field(..., gt=0)


class PedidoItemCreate(PedidoItemBase):
    pass


class PedidoItemResponse(PedidoItemBase):
    id: int
    pedido_id: int
    preco_unitario: float
    subtotal: float

    class Config:
        from_attributes = True


class PedidoCreate(BaseModel):
    cliente_id: int
    canal_pedido: CanalPedidoEnum
    itens: List[PedidoItemCreate]
    observacoes: Optional[str] = None

    @validator("itens")
    def validar_itens_duplicados(cls, v):
        produtos = [item.produto_id for item in v]
        if len(produtos) != len(set(produtos)):
            raise ValueError("Não é permitido produtos duplicados no pedido")
        return v


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


class PedidoListResponse(BaseModel):
    data: List[PedidoResponse]
    page: int
    limit: int
    total: int
    pages: int
    filtros: Optional[dict] = None


class PagamentoRequest(BaseModel):
    pedido_id: int
    metodo: MetodoPagamentoEnum = MetodoPagamentoEnum.MOCK
    detalhes: Optional[dict] = None


class PagamentoResponse(BaseModel):
    pedido_id: int
    status: str
    transacao_id: Optional[str] = None
    mensagem: Optional[str] = None
    processado_em: Optional[datetime] = None


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


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    database: str
    version: str