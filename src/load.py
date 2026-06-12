from sqlalchemy.dialects.sqlite import insert
from src.database import SessionLocal, engine, Base
from src.models import DRE_Model

Base.metadata.create_all(bind=engine)

def load_dre_to_db(df):
    '''Carrega os dados do DataFrame para o banco de dados.'''

    db = SessionLocal()

    try:
        data = df.to_dict(orient="records")

        objects = [DRE_Model(**row) for row in data]

        db.add_all(objects)

        db.commit()

        print(f"{len(data)} registros inseridos")

    except Exception as e:
        db.rollback()
        print(e)

    finally:
        db.close()