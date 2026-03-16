from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Union, List, Dict, Any

from app.core.database import engine
from app.models.models import Base
from app.routes import auth_routes, produtos_routes, pedidos_routes, pagamentos_routes, fidelidade_routes

app = FastAPI(
    title="API Raízes do Nordeste - Sistema de Gestão de Pedidos",
    description="""
    API Back-end para rede de restaurantes Raízes do Nordeste.
    
    ## Funcionalidades
    * Autenticação com JWT
    * Gestão de produtos
    * Criação de pedidos com multicanalidade (APP, TOTEM, BALCÃO, PICKUP, WEB)
    * Pagamento mock (simulação de gateway externo)
    * Programa de fidelidade (pontos a cada R$10)
    * Controle de estoque
    * Auditoria de ações sensíveis
    * Conformidade com LGPD
    """,
    version="1.0.0",
    contact={
        "name": "Gabriel Henrique Pereira Prado",
        "email": "gabriel@email.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS para permitir acesso de diferentes origens
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restrinja para origens específicas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# ========== PADRÃO DE ERRO GLOBAL ==========
class ErrorResponse:
    """Formato padronizado para respostas de erro"""
    
    @staticmethod
    def format(
        error: str,
        message: str,
        status_code: int,
        request: Request = None,
        details: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Formata uma resposta de erro padronizada
        
        Args:
            error: Código do erro (ex: "ESTOQUE_INSUFICIENTE")
            message: Mensagem legível para o usuário
            status_code: Código HTTP do erro
            request: Objeto da requisição (opcional)
            details: Detalhes adicionais do erro (opcional)
        
        Returns:
            Dict com o erro padronizado
        """
        response = {
            "error": error.upper(),
            "message": message,
            "status_code": status_code,
            "timestamp": datetime.now().isoformat(),
        }
        
        if request:
            response["path"] = request.url.path
            response["method"] = request.method
        
        if details:
            response["details"] = details
        
        return response

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Tratamento padronizado para recurso não encontrado"""
    return JSONResponse(
        status_code=404,
        content=ErrorResponse.format(
            error="RECURSO_NAO_ENCONTRADO",
            message="O recurso solicitado não foi encontrado",
            status_code=404,
            request=request
        )
    )

@app.exception_handler(405)
async def method_not_allowed_handler(request: Request, exc):
    """Tratamento padronizado para método não permitido"""
    return JSONResponse(
        status_code=405,
        content=ErrorResponse.format(
            error="METODO_NAO_PERMITIDO",
            message=f"Método {request.method} não permitido para esta rota",
            status_code=405,
            request=request
        )
    )

@app.exception_handler(500)
async def internal_server_error_handler(request: Request, exc):
    """Tratamento padronizado para erro interno do servidor"""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse.format(
            error="ERRO_INTERNO_SERVIDOR",
            message="Ocorreu um erro interno no servidor. Tente novamente mais tarde.",
            status_code=500,
            request=request
        )
    )

# Incluir as rotas
app.include_router(auth_routes.router)
app.include_router(produtos_routes.router)
app.include_router(pedidos_routes.router)
app.include_router(pagamentos_routes.router)
app.include_router(fidelidade_routes.router)

@app.get("/", tags=["Root"])
def root():
    """
    Rota raiz da API
    
    Returns:
        Mensagem de boas-vindas e informações básicas
    """
    return {
        "message": "API Raízes do Nordeste funcionando!",
        "version": "1.0.0",
        "documentacao": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "endpoints_disponiveis": [
            "/auth",
            "/produtos",
            "/pedidos",
            "/pagamentos",
            "/fidelidade"
        ]
    }

@app.get("/health", tags=["Health Check"])
async def health_check():
    """
    Verifica se a API está funcionando corretamente
    
    Returns:
        Status da API e informações do sistema
    """
    try:
        # Testar conexão com o banco de dados
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": db_status,
        "version": "1.0.0"
    }

# Evento de startup
@app.on_event("startup")
async def startup_event():
    """Executado quando a API inicia"""
    print("=" * 50)
    print("🚀 API Raízes do Nordeste iniciada!")
    print(f"📚 Documentação: http://localhost:8000/docs")
    print(f"📖 ReDoc: http://localhost:8000/redoc")
    print("=" * 50)

# Evento de shutdown
@app.on_event("shutdown")
async def shutdown_event():
    """Executado quando a API é encerrada"""
    print("👋 API Raízes do Nordeste encerrada.")