# seed.py atualizado
from app.database import SessionLocal
from app.models import models
from app.models.models import PerfilUsuario
from app.core.security import hash_senha, verificar_senha
from datetime import datetime

def criar_admin_inicial():
    db = SessionLocal()
    
    try:
        # Verificar se já existe admin
        admin = db.query(models.Usuario).filter(models.Usuario.email == "admin@raizes.com").first()
        
        if not admin:
            admin = models.Usuario(
                nome="Administrador",
                email="admin@raizes.com",
                senha=hash_senha("admin123"),
                perfil=PerfilUsuario.ADMIN,
                consentimento_lgpd=True,
                data_consentimento=datetime.now()
            )
            db.add(admin)
            db.commit()
            print("=" * 50)
            print("✅ USUÁRIO ADMIN CRIADO!")
            print("   Email: admin@raizes.com")
            print("   Senha: admin123")
            print("=" * 50)
        else:
            print("=" * 50)
            print("ℹ️ ADMIN JÁ EXISTE")
            print(f"   ID: {admin.id}")
            print(f"   Email: {admin.email}")
            print(f"   Perfil: {admin.perfil.value}")
            
            # Testar a senha
            senha_correta = verificar_senha("admin123", admin.senha)
            print(f"   Senha 'admin123' está correta? {senha_correta}")
            print("=" * 50)
    
    except Exception as e:
        print(f"❌ ERRO: {e}")
    
    finally:
        db.close()

def listar_todos_usuarios():
    db = SessionLocal()
    try:
        usuarios = db.query(models.Usuario).all()
        print("\n" + "=" * 50)
        print("📋 TODOS OS USUÁRIOS:")
        for user in usuarios:
            print(f"   ID: {user.id} | Email: {user.email} | Perfil: {user.perfil.value}")
        print("=" * 50 + "\n")
    except Exception as e:
        print(f"Erro ao listar: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    criar_admin_inicial()
    listar_todos_usuarios()