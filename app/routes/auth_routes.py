from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import UsuarioCreate, UsuarioLogin
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/registrar")
def registrar(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return auth_service.registrar_usuario(db, usuario)

@router.post("/login") 
def login(login: UsuarioLogin, db: Session = Depends(get_db)):
    return auth_service.login_usuario(db, login)

@router.post("/token")  
def login_token(
    username: str = Form(...),  
    password: str = Form(...),  
    db: Session = Depends(get_db)
):
    """
    Endpoint para compatibilidade com OAuth2 (usado pelo botão Authorize do Swagger)
    """
   
    login_data = UsuarioLogin(
        email=username, 
        senha=password   
    )
    return auth_service.login_usuario(db, login_data)