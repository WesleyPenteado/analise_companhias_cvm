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

def ano_mais_recente_dfc(empresa, grupo_dfc):
    '''Retorna o ano mais recente de acordo com a empresa e grupo selecionados'''
    query = f"""
    SELECT MAX(ANO) AS max_ano
    FROM dfc
    WHERE DENOM_CIA = '{empresa}'
    AND GRUPO_DFP = '{grupo_dfc}'
    """
    df = pd.read_sql(query, engine)

    if df.empty or df.iloc[0]["max_ano"] is None:
        return None
    
    return int(df.iloc[0]["max_ano"])

def var_liquida_caixa(empresa, grupo_dfc):
    '''Retorna a variação líquida de caixa de acordo com a empresa e grupo selecionados'''
    query = f"""
    SELECT VL_CONTA
    FROM dfc
    WHERE CD_CONTA = '6.05' -- Conta padrão para variação líquida de caixa 
    AND DENOM_CIA = '{empresa}'
    AND GRUPO_DFP = '{grupo_dfc}'
    ORDER BY ANO DESC
    LIMIT 1
    """
    df = pd.read_sql(query, engine)

    if df.empty or df.iloc[0]["VL_CONTA"] is None:
        return None
    
    return float(df.iloc[0]["VL_CONTA"])