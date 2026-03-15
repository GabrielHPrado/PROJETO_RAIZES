from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
import logging

# CORREÇÃO: Importar diretamente as classes, não o módulo inteiro
from app.schemas.schemas import UsuarioCreate, UsuarioLogin
from app.models import models
from app.core.security import verificar_senha, hash_senha, criar_token

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def registrar_usuario(db: Session, usuario: UsuarioCreate):  # Agora usa a classe diretamente
    try:
        logger.info(f"Tentando registrar usuário: {usuario.email}")
        
        # Validar tamanho da senha
        if len(usuario.senha) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Senha deve ter pelo menos 6 caracteres"
            )
        
        if len(usuario.senha) > 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Senha muito longa (máximo 50 caracteres)"
            )
        
        # Verificar se email já existe
        usuario_existente = db.query(models.Usuario).filter(
            models.Usuario.email == usuario.email
        ).first()
        
        if usuario_existente:
            logger.warning(f"Email já existe: {usuario.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )
        
        # Verificar consentimento LGPD
        if not usuario.consentimento_lgpd:
            logger.warning("Consentimento LGPD não fornecido")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="É necessário aceitar os termos de consentimento LGPD"
            )
        
        # Hash da senha
        try:
            senha_hash = hash_senha(usuario.senha)
            logger.info("Senha hasheada com sucesso")
        except Exception as e:
            logger.error(f"Erro ao fazer hash da senha: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao processar senha"
            )
        
        # Criar usuário
        db_usuario = models.Usuario(
            nome=usuario.nome.strip(),
            email=usuario.email.lower().strip(),
            senha=senha_hash,
            consentimento_lgpd=usuario.consentimento_lgpd,
            data_consentimento=datetime.now() if usuario.consentimento_lgpd else None
        )
        
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        
        logger.info(f"Usuário registrado com sucesso. ID: {db_usuario.id}")
        
        # Retornar usuário sem a senha
        return {
            "id": db_usuario.id,
            "nome": db_usuario.nome,
            "email": db_usuario.email,
            "consentimento_lgpd": db_usuario.consentimento_lgpd,
            "data_consentimento": db_usuario.data_consentimento
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro inesperado no registro: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao registrar usuário: {str(e)}"
        )

def login_usuario(db: Session, login: UsuarioLogin):  # Agora usa a classe diretamente
    try:
        logger.info(f"Tentativa de login: {login.email}")
        
        # Buscar usuário
        usuario = db.query(models.Usuario).filter(
            models.Usuario.email == login.email.lower().strip()
        ).first()
        
        if not usuario:
            logger.warning(f"Usuário não encontrado: {login.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos"
            )
        
        # Verificar senha
        if not verificar_senha(login.senha, usuario.senha):
            logger.warning(f"Senha incorreta para: {login.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos"
            )
        
        # Criar token
        token = criar_token({"sub": str(usuario.id)})
        
        logger.info(f"Login bem-sucedido: {usuario.email}")
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "usuario": {
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao processar login"
        )