from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent  # sobe de src
DB_DIR = BASE_DIR / "data" / "db"

# __ CVM _____________________________________________

CVM_URL = f"sqlite:///{DB_DIR / 'cvm.db'}"

cvm_engine = create_engine(
    CVM_URL,
    connect_args={"check_same_thread": False}
)

cvm_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=cvm_engine
)
cvm_base = declarative_base()


# __ Dependências FastAPI ____________________________

def get__db():
    '''Sessão para o banco da CVM com todas as demonstrações.'''
    db = cvm_session()
    try:
        yield db
    finally:
        db.close()


