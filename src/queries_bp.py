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

def ano_mais_recente_bp(empresa, grupo_bp):
    '''Retorna o ano mais recente de acordo com a empresa e grupo selecionados'''
    query = f"""
    SELECT MAX(ANO) AS max_ano
    FROM bp
    WHERE DENOM_CIA = '{empresa}'
    AND GRUPO_DFP = '{grupo_bp}'
    """
    df = pd.read_sql(query, cvm_engine)

    if df.empty or df.iloc[0]["max_ano"] is None:
        return None
    
    return int(df.iloc[0]["max_ano"])

def tipo_bp(empresa, grupo_bp, ultimo_ano_bp):
    '''Retorna o tipo do balanço patrimonial para a empresa e grupo selecionados'''
    query = f"""
    SELECT tipo_atual
    FROM vw_bp_tipo_empresa
    WHERE DENOM_CIA = '{empresa}'
    AND GRUPO_DFP = '{grupo_bp}'
    AND ANO = {ultimo_ano_bp}
    """
    df = pd.read_sql(query, cvm_engine)

    if df.empty or df.iloc[0]["tipo_atual"] is None:
        return None

    return df.iloc[0]["tipo_atual"]

def ativo_circulante_ou_caixa(empresa, grupo_bp, ultimo_ano_bp):
    '''Retorna o ativo circulante para empresas que não são instituições financeiras e caixa e equivalentes de caixa 
    para instituições financeiras de acordo com a empresa e grupo selecionados'''
    query = f"""
    SELECT VL_CONTA
    FROM bp
    WHERE CD_CONTA = '1.01' -- Conta padrão
    AND DENOM_CIA = '{empresa}'
    AND GRUPO_DFP = '{grupo_bp}'
    AND ANO = {ultimo_ano_bp}
    """
    df = pd.read_sql(query, cvm_engine)

    if df.empty or df.iloc[0]["VL_CONTA"] is None:
        return None

    return float(df.iloc[0]["VL_CONTA"])

def passivo_circulante_ou_financeiro(empresa, grupo_bp, ultimo_ano_bp):
    '''Retorna o passivo circulante para empresas que não são instituições financeiras e passivo financeiro 
    avaliado ao valor justo através de resultado para instituições financeiras de acordo com a empresa e grupo selecionados'''
    query = f"""
    SELECT VL_CONTA
    FROM bp
    WHERE CD_CONTA = '2.01' -- Conta padrão
    AND DENOM_CIA = '{empresa}'
    AND GRUPO_DFP = '{grupo_bp}'
    AND ANO = {ultimo_ano_bp}
    """
    df = pd.read_sql(query, cvm_engine)

    if df.empty or df.iloc[0]["VL_CONTA"] is None:
        return None

    return float(df.iloc[0]["VL_CONTA"])

def ativo_estoques(empresa, grupo_bp, ultimo_ano_bp):
    '''Retorna o valor de estoques para empresas que não são instituições financeiras'''
    query = f"""
    SELECT VL_CONTA
    FROM bp
    WHERE CD_CONTA = '1.01.04' -- Conta padrão para estoques
    AND DENOM_CIA = '{empresa}'
    AND GRUPO_DFP = '{grupo_bp}'
    AND ANO = {ultimo_ano_bp}
    """
    df = pd.read_sql(query, cvm_engine)

    if df.empty or df.iloc[0]["VL_CONTA"] is None:
        return None

    return float(df.iloc[0]["VL_CONTA"])


def passivo_nao_circulante(empresa, grupo_bp, ultimo_ano_bp):
    '''Retorna o passivo não circulante para empresas que não são instituições financeiras de acordo com a empresa e grupo selecionados'''
    query = f"""
    SELECT VL_CONTA
    FROM bp
    WHERE CD_CONTA = '2.02' -- Conta padrão
    AND DENOM_CIA = '{empresa}'
    AND GRUPO_DFP = '{grupo_bp}'
    AND ANO = {ultimo_ano_bp}
    """
    df = pd.read_sql(query, cvm_engine)

    if df.empty or df.iloc[0]["VL_CONTA"] is None:
        return None

    return float(df.iloc[0]["VL_CONTA"])

def patrimonio_liquido(empresa, grupo_bp, ultimo_ano_bp):
    '''Retorna o patrimônio líquido para empresas que não são instituições financeiras de acordo com a empresa e grupo selecionados'''
    query = f"""
    SELECT VL_CONTA
    FROM bp
    WHERE CD_CONTA = '2.03' -- Conta padrão
    AND DENOM_CIA = '{empresa}'
    AND GRUPO_DFP = '{grupo_bp}'
    AND ANO = {ultimo_ano_bp}
    """
    df = pd.read_sql(query, cvm_engine)

    if df.empty or df.iloc[0]["VL_CONTA"] is None:
        return None

    return float(df.iloc[0]["VL_CONTA"])


def ativo_total(empresa, grupo_bp, ultimo_ano_bp):
    '''Retorna o ativo total para empresas que não são instituições financeiras de acordo com a empresa e grupo selecionados'''
    query = f"""
    SELECT VL_CONTA
    FROM bp
    WHERE CD_CONTA = '1' -- Conta padrão
    AND DENOM_CIA = '{empresa}'
    AND GRUPO_DFP = '{grupo_bp}'
    AND ANO = {ultimo_ano_bp}
    """
    df = pd.read_sql(query, cvm_engine)

    if df.empty or df.iloc[0]["VL_CONTA"] is None:
        return None

    return float(df.iloc[0]["VL_CONTA"])



def kpis_evolucao_ativo_passivo_pl(empresa, grupo_bp):
    '''Retorna um data frame com os valores de ativo, passivo e patrimônio líquido para empresas que não são instituições financeiras de acordo com a empresa e grupo selecionados'''
    query = f"""
    SELECT b.CD_CONTA, b.ANO, b.VL_CONTA
    FROM bp b
    INNER JOIN vw_bp_tipo_empresa v
        ON b.DENOM_CIA = v.DENOM_CIA
        AND b.GRUPO_DFP = v.GRUPO_DFP
        AND b.ANO = v.ANO
    WHERE b.DENOM_CIA = '{empresa}'
    AND b.GRUPO_DFP = '{grupo_bp}'
    AND v.tipo_empresa = 'Instituição Não Financeira'
    AND
    (
        b.CD_CONTA = '1.01'
        OR b.CD_CONTA = '1.02'
        OR b.CD_CONTA = '2.01'
        OR b.CD_CONTA = '2.02'
        OR b.CD_CONTA = '2.03'
    )
    ORDER BY b.CD_CONTA,b.ANO;
    """
    df = pd.read_sql(query, cvm_engine)

    return df if not df.empty else pd.DataFrame(columns=["CD_CONTA", "ANO", "VL_CONTA"])



def get_analise_horizontal_bp(empresa, grupo_dfc):
    '''Retorna uma análise horizontal do Balanço Patrimonial para todos os anos disponíveis'''
    query = f"""
    WITH dados AS (
    SELECT
        b.CD_CONTA AS Conta,
        b.DS_CONTA AS Descricao,
        SUM(CASE WHEN b.ANO = 2021 THEN b.VL_CONTA ELSE 0 END) AS Ano_2021,
        SUM(CASE WHEN b.ANO = 2022 THEN b.VL_CONTA ELSE 0 END) AS Ano_2022,
        SUM(CASE WHEN b.ANO = 2023 THEN b.VL_CONTA ELSE 0 END) AS Ano_2023,
        SUM(CASE WHEN b.ANO = 2024 THEN b.VL_CONTA ELSE 0 END) AS Ano_2024,
        SUM(CASE WHEN b.ANO = 2025 THEN b.VL_CONTA ELSE 0 END) AS Ano_2025
    FROM bp b
    INNER JOIN vw_bp_tipo_empresa v
        ON b.DENOM_CIA = v.DENOM_CIA
        AND b.GRUPO_DFP = v.GRUPO_DFP
        AND b.ANO = v.ANO
    WHERE b.DENOM_CIA = '{empresa}'
        AND b.VL_CONTA <> 0
        AND b.GRUPO_DFP = '{grupo_dfc}'
        AND v.tipo_empresa = 'Instituição Não Financeira'
    GROUP BY
        b.CD_CONTA,
        b.DS_CONTA
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
    return pd.read_sql(query, cvm_engine)