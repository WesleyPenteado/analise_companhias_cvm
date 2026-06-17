from src.database import dre_session, dfc_session, dre_engine, dfc_engine, dre_base, dfc_base
from src.models import DRE_Model, DFC_Model

# Cria as tabelas no banco de dados, caso ainda não existam
dre_base.metadata.create_all(bind=dre_engine)
dfc_base.metadata.create_all(bind=dfc_engine)

def load_dre_to_db(df):
    '''Carrega os dados do DataFrame de DRE para o banco de dados.'''

    db = dre_session()

    try:
        db.query(DRE_Model).delete()
        db.commit()

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

    
def load_dfc_to_db(df):
    '''Carrega os dados do DataFrame de fluxo de caixa para o banco de dados.'''

    db = dfc_session()

    try:
        db.query(DFC_Model).delete()
        db.commit()

        data = df.to_dict(orient="records")

        objects = [DFC_Model(**row) for row in data]

        db.add_all(objects)

        db.commit()

        print(f"{len(data)} registros inseridos")

    except Exception as e:
        db.rollback()
        print(e)

    finally:
        db.close()