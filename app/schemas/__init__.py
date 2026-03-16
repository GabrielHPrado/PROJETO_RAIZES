from .schemas import (
    # USUÁRIOS
    UsuarioBase,
    UsuarioCreate,
    UsuarioLogin,
    UsuarioResponse,
    LoginResponse,
    
    # ENUMS
    CanalPedidoEnum,
    StatusPedidoEnum,
    PerfilEnum,
    TipoFidelidadeEnum,
    MetodoPagamentoEnum,
    
    # PRODUTOS
    ProdutoBase,
    ProdutoCreate,
    ProdutoResponse,
    
    # ESTOQUE
    EstoqueBase,
    EstoqueCreate,
    EstoqueResponse,
    EstoqueMovimentacao,
    
    # PEDIDOS (com alias para manter compatibilidade)
    PedidoItemCreate as PedidoItem,  # ALIAS - mantém compatibilidade
    PedidoCreate,
    PedidoResponse,
    PedidoListResponse,
    
    # PAGAMENTOS
    PagamentoRequest,
    PagamentoResponse,
    
    # FIDELIDADE
    FidelidadeBase,
    FidelidadeCreate,
    FidelidadeResponse,
    PontosResponse,
    
    # AUDITORIA
    AuditoriaResponse,
    
    # ERROS
    ErrorDetail,
    ErrorResponse,
    
    # HEALTH
    HealthResponse,
)