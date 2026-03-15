from app.core.security import hash_senha, verificar_senha

def testar_hash():
    senha = "123teste"
    print(f"Testando hash para senha: {senha}")
    
    # Gerar hash
    hashed = hash_senha(senha)
    print(f"Hash gerado: {hashed}")
    print(f"Tamanho do hash: {len(hashed)} caracteres")
    
    # Verificar
    verificacao = verificar_senha(senha, hashed)
    print(f"Verificação: {verificacao}")
    
    # Testar com senha errada
    verificacao_errada = verificar_senha("senha_errada", hashed)
    print(f"Verificação com senha errada: {verificacao_errada}")

if __name__ == "__main__":
    testar_hash()