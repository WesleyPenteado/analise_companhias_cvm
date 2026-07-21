import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent.parent  # sobe de src/
DB_PATH = BASE_DIR / "data" / "db" / "cvm.db"

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL)


def get_grupos_dfc(empresa):
    '''Retorna uma lista de grupos distintos presentes na tabela DFC. Grupos representam os tipos de demonstração: consolidado, individual e o método da análise (direta ou indireta)'''
    query = f"""
    SELECT DISTINCT GRUPO_DFP
    FROM dfc
    WHERE DENOM_CIA = '{empresa}'
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


def caixa_operacional(empresa, grupo_dfc):
    '''Retorna o valor do caixa operacional de acordo com a empresa e grupo selecionados'''
    query = f"""
    SELECT VL_CONTA
    FROM dfc
    WHERE CD_CONTA = '6.01' -- Conta padrão para caixa operacional
    AND DENOM_CIA = '{empresa}'
    AND GRUPO_DFP = '{grupo_dfc}'
    ORDER BY ANO DESC
    LIMIT 1
    """
    df = pd.read_sql(query, engine)

    if df.empty or df.iloc[0]["VL_CONTA"] is None:
        return None
    
    return float(df.iloc[0]["VL_CONTA"])

def caixa_investimento(empresa, grupo_dfc):
    '''Retorna o valor do caixa de investimentos de acordo com a empresa e grupo selecionados'''
    query = f"""
    SELECT VL_CONTA
    FROM dfc
    WHERE CD_CONTA = '6.02' -- Conta padrão para caixa de investimentos
    AND DENOM_CIA = '{empresa}'
    AND GRUPO_DFP = '{grupo_dfc}'
    ORDER BY ANO DESC
    LIMIT 1
    """
    df = pd.read_sql(query, engine)

    if df.empty or df.iloc[0]["VL_CONTA"] is None:
        return None
    
    return float(df.iloc[0]["VL_CONTA"])

def caixa_financiamento(empresa, grupo_dfc):
    '''Retorna o valor do caixa de financiamento de acordo com a empresa e grupo selecionados'''
    query = f"""
    SELECT VL_CONTA
    FROM dfc
    WHERE CD_CONTA = '6.03' -- Conta padrão para caixa de financiamento
    AND DENOM_CIA = '{empresa}'
    AND GRUPO_DFP = '{grupo_dfc}'
    ORDER BY ANO DESC
    LIMIT 1
    """
    df = pd.read_sql(query, engine)

    if df.empty or df.iloc[0]["VL_CONTA"] is None:
        return None
    
    return float(df.iloc[0]["VL_CONTA"])

def var_cambial_equiv(empresa, grupo_dfc):
    '''Retorna o valor de variação cambial e equivalentes de acordo com a empresa e grupo selecionados'''
    query = f"""
    SELECT VL_CONTA
    FROM dfc
    WHERE CD_CONTA = '6.04' -- Conta padrão para variação cambial e equivalentes
    AND DENOM_CIA = '{empresa}'
    AND GRUPO_DFP = '{grupo_dfc}'
    ORDER BY ANO DESC
    LIMIT 1
    """
    df = pd.read_sql(query, engine)

    if df.empty or df.iloc[0]["VL_CONTA"] is None:
        return None
    
    return float(df.iloc[0]["VL_CONTA"])

def valor_capex(empresa, grupo_dfc):
    '''Retorna o valor de capex de acordo com a empresa e grupo selecionados. Query utiliza nomenclaturas de filtro
     que permitem separar o que é capex do que é o caixa de investimento.'''
    query = f"""
    SELECT ANO, SUM(VL_CONTA) AS CAPEX
    FROM dfc
    WHERE DENOM_CIA = '{empresa}'
    AND GRUPO_DFP = '{grupo_dfc}'
    AND
    (
        CD_CONTA LIKE '6.02.0%'
        OR CD_CONTA LIKE '6.02.1%'
        OR CD_CONTA LIKE '6.02.2%'
    )
    AND
    (
        LOWER(ds_conta) LIKE '%aquisi%'
        OR LOWER(ds_conta) LIKE '%adiç%'
        OR LOWER(ds_conta) LIKE '%adição%'
        OR LOWER(ds_conta) LIKE '%aplica%'
        OR LOWER(ds_conta) LIKE '%acréscimo%'
    )
    AND
    (
        LOWER(ds_conta) LIKE '%imobil%'
        OR LOWER(ds_conta) LIKE '%intang%'
        OR LOWER(ds_conta) LIKE '%infraestrutura%'
        OR LOWER(ds_conta) LIKE '%ativo contrat%'
        OR LOWER(ds_conta) LIKE '%software%'
    )
    AND LOWER(ds_conta) NOT LIKE '%aliena%'
    AND LOWER(ds_conta) NOT LIKE '%venda%'
    AND LOWER(ds_conta) NOT LIKE '%recebimento%'
    AND LOWER(ds_conta) NOT LIKE '%baixa%'
    AND LOWER(ds_conta) NOT LIKE '%ganho%'
    AND LOWER(ds_conta) NOT LIKE '%perda%'
    AND LOWER(ds_conta) NOT LIKE '%resultado%'
    AND LOWER(ds_conta) NOT LIKE '%empréstimo%'
    AND LOWER(ds_conta) NOT LIKE '%investimento%'
    AND LOWER(ds_conta) NOT LIKE '%participa%'
    AND LOWER(ds_conta) NOT LIKE '%aplicações financeiras%'
    GROUP BY ANO
    ORDER BY ANO DESC
    LIMIT 1
    """
    df = pd.read_sql(query, engine)

    if df.empty or df.iloc[0]["CAPEX"] is None:
        return None
    
    return float(df.iloc[0]["CAPEX"])


def get_kpis_dfc_todos_os_anos(empresa, grupo_dfc):
    '''Retorna KPI's de caixa (Operacional, investimento, financiamento, variação cambial e equivalentes) e variação líquida de caixa para todos os anos'''
    query = f"""
    SELECT CD_CONTA, ANO, VL_CONTA
    FROM dfc
    WHERE DENOM_CIA = '{empresa}'
    AND GRUPO_DFP = '{grupo_dfc}'
    AND
    (
        CD_CONTA = '6.01'
        OR CD_CONTA = '6.02'
        OR CD_CONTA = '6.03'
        OR CD_CONTA = '6.04'
        OR CD_CONTA = '6.05'
    )
    ORDER BY CD_CONTA,ANO
    """
    df = pd.read_sql(query, engine)

    return df if not df.empty else pd.DataFrame(columns=["CD_CONTA", "ANO", "VL_CONTA"])

def get_analise_horizontal_dfc(empresa, grupo_dfc):
    '''Retorna uma análise horizontal da DFC para todos os anos disponíveis'''
    query = f"""
    WITH dados AS (
    SELECT
        CD_CONTA AS Conta,
        DS_CONTA AS Descricao,
        SUM(CASE WHEN ANO = 2021 THEN VL_CONTA ELSE 0 END) AS Ano_2021,
        SUM(CASE WHEN ANO = 2022 THEN VL_CONTA ELSE 0 END) AS Ano_2022,
        SUM(CASE WHEN ANO = 2023 THEN VL_CONTA ELSE 0 END) AS Ano_2023,
        SUM(CASE WHEN ANO = 2024 THEN VL_CONTA ELSE 0 END) AS Ano_2024,
        SUM(CASE WHEN ANO = 2025 THEN VL_CONTA ELSE 0 END) AS Ano_2025
    FROM dfc
    WHERE DENOM_CIA = '{empresa}'
        AND VL_CONTA <> 0
        AND GRUPO_DFP = '{grupo_dfc}'
    GROUP BY
        CD_CONTA,
        DS_CONTA
    )
    SELECT
        Conta,
        Descricao,
        Ano_2021,
        "-" AS AH_2021,
        Ano_2022,
        ROUND(
            (Ano_2022 - Ano_2021) * 100.0 /
            NULLIF(Ano_2021, 0), 1
        ) AS AH_2022,
        Ano_2023,
        ROUND(
            (Ano_2023 - Ano_2022) * 100.0 /
            NULLIF(Ano_2022, 0), 1
        ) AS AH_2023,
        Ano_2024,
        ROUND(
            (Ano_2024 - Ano_2023) * 100.0 /
            NULLIF(Ano_2023, 0), 1
        ) AS AH_2024,
        Ano_2025,
        ROUND(
            (Ano_2025 - Ano_2024) * 100.0 /
            NULLIF(Ano_2024, 0), 1
        ) AS AH_2025
    FROM dados
    ORDER BY Conta;
    """
    return pd.read_sql(query, engine)

