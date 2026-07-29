import pandas as pd
from src.database import cvm_engine


def get_grupos_bp(empresa):
    '''Retorna uma lista de grupos distintos presentes na tabela BP. Grupos representam os tipos de demonstração: consolidado, individual e o método da análise (direta ou indireta)'''
    query = f"""
    SELECT DISTINCT GRUPO_DFP
    FROM bp
    WHERE DENOM_CIA = '{empresa}'
    ORDER BY GRUPO_DFP
    """

    return pd.read_sql(query, cvm_engine)