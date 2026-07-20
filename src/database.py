from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent  # sobe de src
DB_DIR = BASE_DIR / "data" / "db" 

# __ DRE _____________________________________________

DRE_URL = f"sqlite:///{DB_DIR / 'dre.db'}"

dre_engine = create_engine(
    DRE_URL,
    connect_args={"check_same_thread": False}
)

dre_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=dre_engine
)
dre_base = declarative_base()


# __ DFC _____________________________________________

DFC_URL = f"sqlite:///{DB_DIR / 'dfc.db'}"

dfc_engine = create_engine(
    DFC_URL, 
    connect_args={"check_same_thread": False}
)

dfc_session = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=dfc_engine
)
dfc_base = declarative_base()


# __ BP (Balanço Patrimonial) _____________________________________________

BP_URL = f"sqlite:///{DB_DIR / 'bp.db'}"

bp_engine = create_engine(
    BP_URL, 
    connect_args={"check_same_thread": False}
)

bp_session = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=bp_engine
)
bp_base = declarative_base()


# __ Dependências FastAPI ____________________________

def get__dre_db():
    '''Sessão para o banco da DRE.'''
    db = dre_session()
    try:
        yield db
    finally:
        db.close()

def get__dfc_db():
    '''Sessão para o banco da DFC.'''
    db = dfc_session()
    try:
        yield db
    finally:
        db.close()

def get__bp_db():
    '''Sessão para o banco da BP.'''
    db = bp_session()
    try:
        yield db
    finally:
        db.close()
