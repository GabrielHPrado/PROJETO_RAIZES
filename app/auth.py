from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = "segredo123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_senha(senha: str):
    return pwd_context.hash(senha)


def verificar_senha(senha, senha_hash):
    return pwd_context.verify(senha, senha_hash)


def criar_token(dados: dict):

    dados_token = dados.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    dados_token.update({"exp": expire})

    token = jwt.encode(dados_token, SECRET_KEY, algorithm=ALGORITHM)

    return token