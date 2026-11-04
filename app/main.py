from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.database import engine, Base, SessionLocal
import app.models as models
from app.auth import get_password_hash
from app.routes import admin, public

# 1. Criar tabelas automaticamente no banco SQLite se não existirem
models.Base.metadata.create_all(bind=engine)

# 2. Garantir que a conta 'getulio' esteja criada e com a senha 'getulio1' no banco de dados
def auto_setup_admin():
    db = SessionLocal()
    try:
        user = db.query(models.AdminUser).filter(models.AdminUser.username == "getulio").first()
        if not user:
            user = models.AdminUser(
                username="getulio",
                password_hash=get_password_hash("getulio1"),
                name="Getúlio Ladeira"
            )
            db.add(user)
        else:
            user.password_hash = get_password_hash("getulio1")
        db.commit()
    finally:
        db.close()

auto_setup_admin()

# 3. Inicialização do FastAPI
app = FastAPI(
    title="BIOZON | Purificadores & Assistência Técnica",
    description="Sistema de Gestão Técnica e Portal Público Hidrofiltros Fortaleza",
    version="1.0.0"
)

# 4. Middleware para controle de sessões de login do admin
app.add_middleware(
    SessionMiddleware,
    secret_key="biozon-fortaleza-chave-secreta-getulio-ladeira-2026"
)

# 5. Mapeamento de arquivos estáticos (CSS, JS, Vídeos e Imagens)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 6. Registro dos roteadores modulares
app.include_router(public.router)
app.include_router(admin.router)

