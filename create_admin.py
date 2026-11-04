from app.database import SessionLocal, engine
from app.models import AdminUser, Base
from app.auth import get_password_hash

# Garante a criação de todas as tabelas no SQLite
Base.metadata.create_all(bind=engine)

def init_admin():
    db = SessionLocal()
    username = "getulio"
    password = "SuaSenhaSeguraAqui123"

    existing = db.query(AdminUser).filter(AdminUser.username == username).first()
    if not existing:
        user = AdminUser(
            username=username,
            password_hash=get_password_hash(password),
            name="Getúlio Ladeira"
        )
        db.add(user)
        db.commit()
        print(f"Sucesso: Usuário '{username}' criado com a senha de acesso configurada!")
    else:
        print(f"Aviso: O usuário '{username}' já existe no banco de dados.")

    db.close()

if __name__ == "__main__":
    init_admin()

    