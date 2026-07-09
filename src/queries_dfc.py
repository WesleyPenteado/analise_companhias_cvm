import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent  # sobe de src/
DB_PATH = BASE_DIR / "data" / "db" / "dfc.db"

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL)


def get_grupos_dfc():
    '''Retorna uma lista de grupos distintos presentes na tabela DFC. Grupos representam os tipos de demonstração: consolidado, individual e o método da análise (direta ou indireta)'''
    query = """
    SELECT DISTINCT GRUPO_DFP
    FROM dfc
    ORDER BY GRUPO_DFP
    """

    return pd.read_sql(query, engine)

