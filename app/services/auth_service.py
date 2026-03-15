from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app import models, schemas
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

SECRET_KEY = "seu-segredo-aqui"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_senha(senha_plana, senha_hash):
    return pwd_context.verify(senha_plana, senha_hash)

def gerar_hash_senha(senha):
    return pwd_context.hash(senha)

def criar_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def registrar_usuario(db: Session, usuario: schemas.UsuarioCreate):
    if db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first():
        raise HTTPException(status_code=400, detail="Email já existe")
    
    if not usuario.consentimento_lgpd:
        raise HTTPException(status_code=400, detail="Consentimento LGPD obrigatório")
    
    db_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=gerar_hash_senha(usuario.senha),
        consentimento_lgpd=usuario.consentimento_lgpd,
        data_consentimento=datetime.now() if usuario.consentimento_lgpd else None
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def login_usuario(db: Session, login: schemas.UsuarioLogin):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == login.email).first()
    if not usuario or not verificar_senha(login.senha, usuario.senha):
        raise HTTPException(
            status_code=401,
            detail="Email ou senha incorretos"
        )
    
    token = criar_token({"sub": str(usuario.id)})
    return {"access_token": token, "token_type": "bearer"}