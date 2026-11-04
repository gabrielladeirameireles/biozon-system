from app.database import engine, Base
import app.models as models

print("Recriando a estrutura do banco SQLite com o campo 'equipment'...")
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print("Banco de dados sincronizado com sucesso!")

