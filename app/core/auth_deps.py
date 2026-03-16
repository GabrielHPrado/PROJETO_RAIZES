from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models import models
from app.core.config import settings
from app.core.security import SECRET_KEY, ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token") 

async def get_usuario_atual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.Usuario:
    """
    Obtém o usuário atual a partir do token JWT
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
       
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id: str = payload.get("sub")
        if usuario_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
 
    usuario = db.query(models.Usuario).filter(models.Usuario.id == int(usuario_id)).first()
    if usuario is None:
        raise credentials_exception
    
    return usuario

def requer_perfil(perfis_permitidos: list):
    """
    Decorator para verificar se o usuário tem o perfil necessário
    Uso: @requer_perfil(["ADMIN", "GERENTE"])
    """
    async def perfil_dependency(
        usuario_atual: models.Usuario = Depends(get_usuario_atual)
    ):
        if usuario_atual.perfil.value not in perfis_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "ACESSO_NEGADO",
                    "message": f"Perfil necessário: {', '.join(perfis_permitidos)}",
                    "seu_perfil": usuario_atual.perfil.value
                }
            )
        return usuario_atual
    return perfil_dependency

def requer_admin(usuario_atual: models.Usuario = Depends(get_usuario_atual)):
    if usuario_atual.perfil.value != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "ACESSO_NEGADO",
                "message": "Apenas administradores podem acessar este recurso",
                "seu_perfil": usuario_atual.perfil.value
            }
        )
    return usuario_atual

def requer_gerente_ou_admin(usuario_atual: models.Usuario = Depends(get_usuario_atual)):
    if usuario_atual.perfil.value not in ["ADMIN", "GERENTE"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "ACESSO_NEGADO",
                "message": "Apenas gerentes ou administradores podem acessar este recurso",
                "seu_perfil": usuario_atual.perfil.value
            }
        )
    return usuario_atual