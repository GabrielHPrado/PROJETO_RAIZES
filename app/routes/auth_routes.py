from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas
from app.services import auth_service
# NÃO PRECISA DE models AQUI porque só usa o service

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/registrar")
def registrar(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return auth_service.registrar_usuario(db, usuario)

@router.post("/login")
def login(login: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    return auth_service.login_usuario(db, login)