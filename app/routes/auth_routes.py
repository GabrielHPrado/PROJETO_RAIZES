from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import UsuarioCreate, UsuarioLogin
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/registrar")
def registrar(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return auth_service.registrar_usuario(db, usuario)

@router.post("/login")  # Seu endpoint original (com email/senha)
def login(login: UsuarioLogin, db: Session = Depends(get_db)):
    return auth_service.login_usuario(db, login)

@router.post("/token")  # NOVO ENDPOINT para o Swagger Authorize
def login_token(
    username: str = Form(...),  # O Swagger envia como 'username'
    password: str = Form(...),  # O Swagger envia como 'password'
    db: Session = Depends(get_db)
):
    """
    Endpoint para compatibilidade com OAuth2 (usado pelo botão Authorize do Swagger)
    """
    # Converte username/email para o formato esperado
    login_data = UsuarioLogin(
        email=username,  # Mapeia username para email
        senha=password   # Mapeia password para senha
    )
    return auth_service.login_usuario(db, login_data)