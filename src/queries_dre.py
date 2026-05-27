import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent  # sobe de src/
DB_PATH = BASE_DIR / "data" / "db" / "dre.db"

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL)


def get_empresas():
    query = """
    SELECT DISTINCT DENOM_CIA
    FROM dre
    ORDER BY DENOM_CIA
    """

    return pd.read_sql(query, engine)

def get_grupos():
    query = """
    SELECT DISTINCT GRUPO_DFP
    FROM dre
    ORDER BY GRUPO_DFP
    """

    return pd.read_sql(query, engine)

def ano_mais_recente(empresa, grupo):
    query = f"""
    SELECT MAX(ANO) AS max_ano
    FROM dre
    WHERE DENOM_CIA = '{empresa}'
    AND GRUPO_DFP = '{grupo}'
    """
    df = pd.read_sql(query, engine)

    if df.empty or df.iloc[0]["max_ano"] is None:
        return None
    
    return int(df.iloc[0]["max_ano"])



def get_receita_card(empresa, grupo):
    
    query = f"""
    WITH ultimo_ano_empresa AS (
        SELECT MAX(ANO) AS max_ano
        FROM dre
        WHERE DENOM_CIA = '{empresa}'
        AND GRUPO_DFP = '{grupo}'
    )
    SELECT
    VL_CONTA
    FROM dre
    WHERE CD_CONTA = '3.01'
    AND ANO = (SELECT max_ano FROM ultimo_ano_empresa)
    AND DENOM_CIA = '{empresa}'
    AND GRUPO_DFP = '{grupo}';
    """
    df = pd.read_sql(query, engine)

    if not df.empty:
        return float(df.iloc[0]["VL_CONTA"])
    
    return 0

def get_mg_bruta_card(empresa, grupo):
    query = f"""
    WITH ultimo_ano_empresa AS (
        SELECT MAX(ANO) AS max_ano
        FROM dre
        WHERE DENOM_CIA = '{empresa}'
        AND GRUPO_DFP = '{grupo}'
    )
    SELECT
    VL_CONTA
    FROM dre
    WHERE CD_CONTA = '3.03'
    AND ANO = (SELECT max_ano FROM ultimo_ano_empresa)
    AND DENOM_CIA = '{empresa}'
    AND GRUPO_DFP = '{grupo}';
    """
    df = pd.read_sql(query, engine)

    if not df.empty:
        return float(df.iloc[0]["VL_CONTA"])
    
    return 0

def get_ebit_card(empresa, grupo):
    
    query = f"""
    WITH ultimo_ano_empresa AS (
        SELECT MAX(ANO) AS max_ano
        FROM dre
        WHERE DENOM_CIA = '{empresa}'
        AND GRUPO_DFP = '{grupo}'
    )
    SELECT
    VL_CONTA
    FROM dre
    WHERE 
    (DS_CONTA LIKE "%Resultado Antes do Resultado%" OR DS_CONTA LIKE "%Resultado Antes dos Tributos%")
    AND ANO = (SELECT max_ano FROM ultimo_ano_empresa)
    AND DENOM_CIA = '{empresa}'
    AND GRUPO_DFP = '{grupo}'
    ORDER BY 
    CASE 
        WHEN DS_CONTA LIKE '%Resultado Antes do Resultado%' THEN 1
        ELSE 2
    END
    LIMIT 1;
    """
    df = pd.read_sql(query, engine)

    if not df.empty:
        return float(df.iloc[0]["VL_CONTA"])
    
    return 0

def get_ebitda_card(empresa, grupo):
    
    query = f"""
    WITH ultimo_ano_empresa AS (
        SELECT MAX(ANO) AS max_ano
        FROM dre
        WHERE DENOM_CIA = '{empresa}'
        AND GRUPO_DFP = '{grupo}'
    )
    SELECT
    COALESCE(SUM(VL_CONTA), 0) AS VL_CONTA 
    FROM dre
    WHERE 
    (DS_CONTA LIKE "%Deprecia%" OR DS_CONTA LIKE "%Amort%" OR DS_CONTA LIKE "%Provisão%")
    AND ANO = (SELECT max_ano FROM ultimo_ano_empresa)
    AND SUBSTR(CD_CONTA, 1, 4) <= '3.04' -- somente contas de resultado operacional no filtro
    AND DENOM_CIA = '{empresa}'
    AND GRUPO_DFP = '{grupo}';
    """
    df = pd.read_sql(query, engine)

    if not df.empty:
        return float(df.iloc[0]["VL_CONTA"]) * -1 # invertendo sinal para somar ao EBIT depois
    
    return 0


def get_lucro_liquido(empresa, grupo):
    query = f"""
    WITH ultimo_ano_empresa AS (
        SELECT MAX(ANO) AS max_ano
        FROM dre
        WHERE DENOM_CIA = '{empresa}'
        AND GRUPO_DFP = '{grupo}'
    )
    SELECT
    VL_CONTA
    FROM dre
    WHERE CD_CONTA = '3.11'
    AND ANO = (SELECT max_ano FROM ultimo_ano_empresa)
    AND DENOM_CIA = '{empresa}'
    AND GRUPO_DFP = '{grupo}';
    """
    df = pd.read_sql(query, engine)

    if not df.empty:
        return float(df.iloc[0]["VL_CONTA"])
    
    return 0




def get_dre_empresa(empresa, grupo):
    
    query = f"""
    SELECT
        CD_CONTA AS Conta,
        DS_CONTA AS Descricao,

        SUM(CASE WHEN ANO = 2021 THEN VL_CONTA ELSE 0 END) AS Ano_2021,
        SUM(CASE WHEN ANO = 2022 THEN VL_CONTA ELSE 0 END) AS Ano_2022,
        SUM(CASE WHEN ANO = 2023 THEN VL_CONTA ELSE 0 END) AS Ano_2023,
        SUM(CASE WHEN ANO = 2024 THEN VL_CONTA ELSE 0 END) AS Ano_2024,
        SUM(CASE WHEN ANO = 2025 THEN VL_CONTA ELSE 0 END) AS Ano_2025

    FROM dre

    WHERE
        DENOM_CIA = '{empresa}'
        AND VL_CONTA <> 0
        AND GRUPO_DFP = '{grupo}'

    GROUP BY
        CD_CONTA,
        DS_CONTA

    ORDER BY
        CD_CONTA
    """

    return pd.read_sql(query, engine)
