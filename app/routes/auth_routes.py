from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import UsuarioCreate, UsuarioLogin  # Imports diretos
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/registrar")
def registrar(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return auth_service.registrar_usuario(db, usuario)

@router.post("/login")
def login(login: UsuarioLogin, db: Session = Depends(get_db)):
    return auth_service.login_usuario(db, login)