from app.database import SessionLocal, engine
from app.models import AdminUser, Base
from app.auth import get_password_hash

Base.metadata.create_all(bind=engine)

def reset_password():
    db = SessionLocal()
    username = "getulio"
    new_password = "getulio1"

    user = db.query(AdminUser).filter(AdminUser.username == username).first()
    if user:
        user.password_hash = get_password_hash(new_password)
        db.commit()
        print(f"Sucesso: Senha do usuário '{username}' redefinida para '{new_password}'!")
    else:
        user = AdminUser(
            username=username,
            password_hash=get_password_hash(new_password),
            name="Getúlio Ladeira"
        )
        db.add(user)
        db.commit()
        print(f"Sucesso: Usuário '{username}' criado com a senha '{new_password}'!")

    db.close()

if __name__ == "__main__":
    reset_password()

    