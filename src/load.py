from database import SessionLocal
from models import DRE_Model

def load_dre_to_db(df):
    db = SessionLocal()
    try:
        data = df.to_dict(orient="records")
        db.bulk_insert_mappings(DRE_Model, data)
        db.commit()
        print(f"{len(data)} registros inseridos")
    except Exception as e:
        db.rollback()
        print(e)
    finally:
        db.close()