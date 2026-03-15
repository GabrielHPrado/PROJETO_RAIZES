from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Usuario
from schemas import UsuarioCreate
from auth import hash_senha, verificar_senha, criar_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(user: UsuarioCreate, db: Session = Depends(get_db)):

    novo = Usuario(
        email=user.email,
        senha=hash_senha(user.senha)
    )

    db.add(novo)
    db.commit()

    return {"msg": "usuario criado"}


@router.post("/login")
def login(user: UsuarioCreate, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(
        Usuario.email == user.email
    ).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="usuario não encontrado")

    if not verificar_senha(user.senha, usuario.senha):
        raise HTTPException(status_code=401, detail="senha incorreta")

    token = criar_token({"sub": usuario.email})

    return {"access_token": token}