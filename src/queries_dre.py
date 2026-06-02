import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent  # sobe de src/
DB_PATH = BASE_DIR / "data" / "db" / "dre.db"

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL)


def get_empresas():
    '''Retorna uma lista de empresas distintas presentes na tabela DRE.'''
    query = """
    SELECT DISTINCT DENOM_CIA
    FROM dre
    ORDER BY DENOM_CIA
    """

    return pd.read_sql(query, engine)

def get_grupos():
    '''Retorna uma lista de grupos distintos presentes na tabela DRE. Grupos representam os tipos de demonstração: consolidado, individual e etc'''
    query = """
    SELECT DISTINCT GRUPO_DFP
    FROM dre
    ORDER BY GRUPO_DFP
    """

    return pd.read_sql(query, engine)

def ano_mais_recente(empresa, grupo):
    '''Retorna o ano mais recente de acordo com a empresa e grupo selecionados'''
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
    '''Retorna a receita líquida mais recente de acordo com a empresa e grupo selecionados'''
    
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
    '''Retorna a margem bruta mais recente de acordo com a empresa e grupo selecionados'''
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
    '''Retorna o EBIT mais recente de acordo com a empresa e grupo selecionados'''
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
    '''Retorna o EBITDA mais recente de acordo com a empresa e grupo selecionados. Leva em consideração um ajuste de depreciação, amortização e provisões para chegar no valor do EBITDA'''
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
    (DS_CONTA LIKE "%Deprecia%" OR DS_CONTA LIKE "%Amort%" OR DS_CONTA LIKE "%Provis%")
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
    '''Retorna o lucro líquido mais recente de acordo com a empresa e grupo selecionados'''
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

def get_receita_todos_os_anos(empresa, grupo):
    '''Retorna a receita líquida de todos os anos disponíveis de acordo com a empresa e grupo selecionados'''
    
    query = f"""
    SELECT
    ANO,
    VL_CONTA
    FROM dre
    WHERE CD_CONTA = '3.01' AND VL_CONTA > 0
    AND DENOM_CIA = '{empresa}'
    AND GRUPO_DFP = '{grupo}';
    """
    df = pd.read_sql(query, engine)

    return df if not df.empty else pd.DataFrame(columns=["ANO", "VL_CONTA"])


def get_kpis_todos_os_anos(empresa, grupo):
    '''Retorna a margem bruta, EBITDA e lucro líquido em percentuais de todos os anos disponíveis de acordo com a empresa e grupo selecionados'''
    query = f"""
    WITH rec_liq as(
    SELECT
        ANO,
        VL_CONTA AS REC_LIQ
    FROM dre
    WHERE CD_CONTA = '3.01'
    AND DENOM_CIA LIKE '%BCO BRASIL S.A%'
    AND GRUPO_DFP = 'DF Consolidado - Demonstração do Resultado'
    ),
    margem_bruta as (
    SELECT
        ANO,
        VL_CONTA AS MG_BRUTA
    FROM dre
    WHERE CD_CONTA = '3.03'
    AND DENOM_CIA LIKE '%BCO BRASIL S.A%'
    AND GRUPO_DFP = 'DF Consolidado - Demonstração do Resultado'
    ),
    ebit AS (
    SELECT ANO, EBIT
    FROM (
        SELECT
            ANO,
            VL_CONTA AS EBIT,
            ROW_NUMBER() OVER (
                PARTITION BY ANO
                ORDER BY
                    CASE
                        WHEN DS_CONTA LIKE '%Resultado Antes do Resultado%' THEN 1
                        WHEN DS_CONTA LIKE '%Resultado Antes dos Tributos%' THEN 2
                        ELSE 3
                    END
            ) AS rn
        FROM dre
        WHERE 
            (DS_CONTA LIKE '%Resultado Antes do Resultado%'
            OR DS_CONTA LIKE '%Resultado Antes dos Tributos%')
            AND DENOM_CIA LIKE '%BCO BRASIL S.A%'
            AND GRUPO_DFP = 'DF Consolidado - Demonstração do Resultado'
    )
    WHERE rn = 1
    ),
    ajuste_ebitda AS (
    SELECT
        ANO,
        COALESCE(SUM(VL_CONTA), 0) AS AJUSTE 
    FROM dre
    WHERE 
    (DS_CONTA LIKE "%Deprecia%" OR DS_CONTA LIKE "%Amort%" OR DS_CONTA LIKE "%Provis%")
    AND SUBSTR(CD_CONTA, 1, 4) <= '3.04' -- somente contas de resultado operacional no filtro
    AND DENOM_CIA LIKE '%BCO BRASIL S.A%'
    AND GRUPO_DFP = 'DF Consolidado - Demonstração do Resultado'
    GROUP BY ANO
    ),
    lucro_liquido AS (
    SELECT
    ANO,
    VL_CONTA AS LUCRO_LIQ
    FROM dre
    WHERE CD_CONTA = '3.11'
    AND DENOM_CIA LIKE '%BCO BRASIL S.A%'
    AND GRUPO_DFP = 'DF Consolidado - Demonstração do Resultado'
    )
    SELECT
        r.ANO,
        ROUND(
            (CAST(m.MG_BRUTA AS REAL) / CAST(r.REC_LIQ AS REAL)) * 100,
            1
        ) AS MG_BRUTA,
        ROUND(
            ((CAST(e.EBIT AS REAL) - COALESCE(a.AJUSTE, 0)) / CAST(r.REC_LIQ AS REAL) * 100),
            1
        ) AS EBITDA,
        ROUND(
            (CAST(l.LUCRO_LIQ AS REAL) / CAST(r.REC_LIQ AS REAL)) * 100,
            1
        ) AS LUCRO_LIQ
    FROM rec_liq r
    LEFT JOIN margem_bruta m ON r.ANO = m.ANO
    LEFT JOIN ebit e ON r.ANO = e.ANO
    LEFT JOIN ajuste_ebitda a ON r.ANO = a.ANO
    LEFT JOIN lucro_liquido l on r.ANO = l.ANO
    ORDER BY r.ANO;
    """
    
    df = pd.read_sql(query, engine)

    return df if not df.empty else pd.DataFrame(columns=["ANO", "MG_BRUTA", "EBITDA", "LUCRO_LIQ"])


def get_dre_empresa(empresa, grupo):
    '''Retorna a tabela de DRE contemplando todas as contas e anos disponíveis de acordo com a empresa e grupo selecionados'''
    
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
