
from src.database import cvm_engine


def create_bp_views():
    '''Cria as views no banco de dados para o balanço patrimonial.
    - 1ª view: vw_bp_tipo_anual - Classifica as empresas em Instituição Financeira ou Instituição Não Financeira com base no 
    valor da conta 1.01 "Caixa e Equivalentes de Caixa" do balanço patrimonial e considerando o ano.
    - 2ª view: vw_bp_tipo_empresa - Cria a coluna "considerar" que indica 1 para os tipos de empresa que são iguais ao tipo 
    mais recente ou iguais ao último ano.
    '''

    sql_views = [

        """
        DROP VIEW IF EXISTS vw_bp_tipo_anual;
        """,

        """
        CREATE VIEW vw_bp_tipo_anual AS
        SELECT
            DENOM_CIA,
            GRUPO_DFP,
            ANO,
            CASE
                WHEN DS_CONTA = 'Caixa e Equivalentes de Caixa'
                    THEN 'Instituição Financeira'
                WHEN DS_CONTA = 'Ativo Circulante'
                    THEN 'Instituição Não Financeira'
            END AS tipo_empresa
        FROM bp
        WHERE CD_CONTA = '1.01';
        """,

        """
        DROP VIEW IF EXISTS vw_bp_tipo_empresa;
        """,

        """
        CREATE VIEW vw_bp_tipo_empresa AS

        WITH ultimo_ano AS (

            SELECT
                DENOM_CIA,
                GRUPO_DFP,
                MAX(ANO) AS ultimo_ano

            FROM vw_bp_tipo_anual

            GROUP BY
                DENOM_CIA,
                GRUPO_DFP
        ),

        tipo_atual AS (

            SELECT
                b.DENOM_CIA,
                b.GRUPO_DFP,
                b.tipo_empresa AS tipo_atual

            FROM vw_bp_tipo_anual b

            INNER JOIN ultimo_ano u

                ON b.DENOM_CIA = u.DENOM_CIA
                AND b.GRUPO_DFP = u.GRUPO_DFP
                AND b.ANO = u.ultimo_ano
        )

        SELECT

            b.DENOM_CIA,
            b.GRUPO_DFP,
            b.ANO,

            b.tipo_empresa,
            t.tipo_atual,

            CASE
                WHEN b.tipo_empresa = t.tipo_atual
                    THEN 1
                ELSE 0
            END AS considerar

        FROM vw_bp_tipo_anual b

        INNER JOIN tipo_atual t

            ON b.DENOM_CIA = t.DENOM_CIA
            AND b.GRUPO_DFP = t.GRUPO_DFP;

        """
    ]


    with cvm_engine.connect() as conn:

        for sql in sql_views:
            conn.exec_driver_sql(sql)

        conn.commit()

