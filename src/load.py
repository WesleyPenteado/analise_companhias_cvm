from src.database import cvm_session, cvm_engine, cvm_base
from src.models import DRE_Model, DFC_Model, BP_Model

# Cria as tabelas no banco de dados, caso ainda não existam
cvm_base.metadata.create_all(bind=cvm_engine)

def load_dre_to_db(df):
    '''Carrega os dados do DataFrame de DRE para o banco de dados.'''

    db = cvm_session()

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

    db = cvm_session()

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


def load_bp_to_db(df):
    '''Carrega os dados do DataFrame de balanço patrimonial para o banco de dados.'''

    db = cvm_session()

    try:
        db.query(BP_Model).delete()
        db.commit()

        data = df.to_dict(orient="records")

        objects = [BP_Model(**row) for row in data]

        db.add_all(objects)

        db.commit()

        print(f"{len(data)} registros inseridos")

    except Exception as e:
        db.rollback()
        print(e)

    finally:
        db.close()