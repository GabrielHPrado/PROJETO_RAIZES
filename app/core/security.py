from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import bcrypt

SECRET_KEY = "segredo123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Configurar o CryptContext com bcrypt explícito
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Número de rounds (padrão é 12)
)

def hash_senha(senha: str) -> str:
    """
    Gera hash da senha usando bcrypt
    """
    if not senha:
        raise ValueError("Senha não pode ser vazia")
    
    # Garantir que a senha seja codificada corretamente
    if isinstance(senha, str):
        senha = senha.encode('utf-8')
    
    # Gerar salt e hash
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(senha, salt)
    
    return hashed.decode('utf-8')

def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """
    Verifica se a senha corresponde ao hash
    """
    if not senha_plana or not senha_hash:
        return False
    
    # Garantir codificação correta
    if isinstance(senha_plana, str):
        senha_plana = senha_plana.encode('utf-8')
    if isinstance(senha_hash, str):
        senha_hash = senha_hash.encode('utf-8')
    
    try:
        return bcrypt.checkpw(senha_plana, senha_hash)
    except Exception as e:
        print(f"Erro ao verificar senha: {e}")
        return False

def criar_token(dados: dict) -> str:
    """
    Cria um token JWT
    """
    dados_token = dados.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados_token.update({"exp": expire})
    token = jwt.encode(dados_token, SECRET_KEY, algorithm=ALGORITHM)
    return token

gerar_hash_senha = hash_senha