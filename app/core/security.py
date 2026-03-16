from datetime import datetime, timedelta
from jose import jwt
import bcrypt

SECRET_KEY = "abacate0709"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def hash_senha(senha: str) -> str:
    
    if senha == "":
        raise ValueError("Senha vazia")

    senha_bytes = senha.encode("utf-8")
    salt = bcrypt.gensalt()
    senha_hash = bcrypt.hashpw(senha_bytes, salt)

    return senha_hash.decode("utf-8")


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    
    try:
        senha_bytes = senha_plana.encode("utf-8")
        hash_bytes = senha_hash.encode("utf-8")

        return bcrypt.checkpw(senha_bytes, hash_bytes)

    except:
        return False


def criar_token(dados: dict):
    
    payload = dados.copy()
    expira = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload["exp"] = expira

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


gerar_hash_senha = hash_senha