import streamlit as st

from src.utils.components import (
    kpi_card,
    line_chart
)
from src.utils.formatters import (
    formatar_brl_tabela,
    format_brl,
    formatar_variacao
)
from src.queries_dre import (
    get_empresas,
    get_grupos_dre,
    get_dre_empresa,
    get_receita_card,
    ano_mais_recente,
    get_mg_bruta_card,
    get_ebit_card,
    get_ebitda_card,
    get_lucro_liquido,
    get_receita_todos_os_anos,
    get_kpis_todos_os_anos,
    get_analise_horizontal_dre,
    get_analise_vertical_dre
)

from src.queries_dfc import (
    get_grupos_dfc,
    ano_mais_recente_dfc,
    var_liquida_caixa,
    caixa_operacional,
    caixa_investimento,
    caixa_financiamento,
    var_cambial_equiv,
    valor_capex,
    get_kpis_dfc_todos_os_anos,
    get_analise_horizontal_dfc
)

from src.queries_bp import (
    get_grupos_bp
)

# ====================================
# CONFIG
# ====================================

st.set_page_config(
    page_title="Dashboard CVM",
    layout="wide"
)

# ====================================
# SIDEBAR
# ====================================

st.sidebar.title("Análise das Demonstrações Financeiras")

empresas_df = get_empresas()
grupos_df = get_grupos_dre()

empresa = st.sidebar.selectbox(
    "Escolha a empresa",
    empresas_df["DENOM_CIA"]
)



st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "Selecione a demonstração:",
    [
        "DRE",
        "Fluxo de Caixa",
        "Balanço Patrimonial"
    ]
)



# ====================================
# DRE
# ====================================

if pagina == "DRE":

    st.title("📊 DRE - Demonstração do Resultado do Exercício")

    grupo_dre = st.selectbox(
        "Selecione o grupo da DRE",
        grupos_df["GRUPO_DFP"]
    )


    # ====================================
    # CARDS TOPO PÁGINA
    # ====================================  
    
    ultimo_ano_dre = ano_mais_recente(empresa, grupo_dre)

    if ultimo_ano_dre:
        st.markdown(
            f"""
            <ul style='
                color: gray;
                font-size: 0.85em;
                padding-left: 18px;
                margin-top: 25px;
                margin-bottom: 0;
            '>
                <li style='margin-bottom: 2px;'>
                    KPI's referentes ao ano mais recente disponível: {ultimo_ano_dre}.
                </li>
                <li>
                    Valores expressos em R$ mil
                </li>
            </ul>
            """,
            unsafe_allow_html=True
        )

    else:
        st.warning("Nenhum dado disponível para a empresa e grupo selecionados.")


    

    # Colunas para os cards ficarem lado a lado
    col1, col2, col3, col4 = st.columns(4)
    
    # Valores inteiros
    v_receita = get_receita_card(empresa, grupo_dre)
    v_mg_bruta = get_mg_bruta_card(empresa, grupo_dre)
    v_ebit = get_ebit_card(empresa, grupo_dre)
    v_ebitda = get_ebitda_card(empresa, grupo_dre)
    v_ebitda = v_ebit + v_ebitda
    v_lucro_liquido = get_lucro_liquido(empresa, grupo_dre)

    # Formata o número no padrão brasileiro
    valor_formatado1 = format_brl(v_receita)
    valor_formatado2 = format_brl(v_mg_bruta)
    valor_formatado3 = format_brl(v_ebitda)
    valor_formatado4 = format_brl(v_lucro_liquido)

    # KPI's percentuais
    perc_mg_bruta = (v_mg_bruta / v_receita) * 100 if v_receita else 0
    perc_ebitda = (v_ebitda / v_receita) * 100 if v_receita else 0
    perc_lucro_liquido = (v_lucro_liquido / v_receita) * 100 if v_receita else 0

    
    with col1:
        kpi_card("Receita Líquida", valor_formatado1)

    with col2:
        kpi_card("Margem Bruta", valor_formatado2, perc_mg_bruta)
 
    with col3:
        kpi_card("EBITDA", valor_formatado3, perc_ebitda)

    with col4:
        kpi_card("Lucro Líquido", valor_formatado4, perc_lucro_liquido)

    

    # ====================================
    # Gráficos de Linha
    # ====================================     
    
    # Colunas para os gráficos ficarem lado a lado
    col1, col2 = st.columns(2)

    with col1:
        df = get_receita_todos_os_anos(empresa, grupo_dre)
    
        line_chart(
            df=df,
            col_x="ANO",
            series=[{"col": "VL_CONTA", "label": "Receita Líquida"}],
            titulo="Receita Líquida x Ano",
            formato_y="monetario",
        )

    with col2:
        df = get_kpis_todos_os_anos(empresa, grupo_dre)

        line_chart(
            df=df,
            col_x="ANO",
            series=[
                {"col": "MG_BRUTA", "label": "Margem Bruta"},
                {"col": "EBITDA", "label": "EBITDA"},
                {"col": "LUCRO_LIQ", "label": "Lucro Líquido"}
            ],
            titulo="Evolução KPI's x Ano",
            formato_y="percentual",
        )

    
    # ====================================
    # Tabela completa DRE
    # ====================================    

    st.subheader("📈 Análise Horizontal DRE")

    df = get_analise_horizontal_dre(empresa, grupo_dre)

    st.markdown(
    """
    <p style='text-align: right;
    color: gray;
    font-size: 0.85em;'>
    Valores expressos em R$ mil
    </p>
    """,
    unsafe_allow_html=True
    )

    df_fmt = formatar_brl_tabela(df)

    st.dataframe(
        formatar_variacao(df_fmt),
        use_container_width=True,
        hide_index=True
    )


    st.subheader("📈 Análise Vertical DRE")

    df = get_analise_vertical_dre(empresa, grupo_dre)
    
    st.markdown(
    """
    <p style='text-align: right;
    color: gray;
    font-size: 0.85em;'>
    Valores expressos em R$ mil
    </p>
    """,
    unsafe_allow_html=True
    )

    df_fmt = formatar_brl_tabela(df)

    st.dataframe(
        formatar_variacao(df_fmt),
        use_container_width=True,
        hide_index=True
    )



# ====================================
# DFC
# ====================================

elif pagina == "Fluxo de Caixa":

    st.title("💰 Fluxo de Caixa")

    st.markdown(
        """
        <p style='text-align: left;
        color: red;
        font-size: 1,5em;'>
        RELATÓRIO EM CONSTRUÇÃO.
        </p>
        """,
        unsafe_allow_html=True
    )

    grupos_df = get_grupos_dfc(empresa)

    grupo_dfc = st.selectbox(
        "Grupo e método do fluxo de caixa",
        grupos_df["GRUPO_DFP"]
    )

    # ====================================
    # CARDS TOPO PÁGINA
    # ====================================  
    
    ultimo_ano_dfc = ano_mais_recente_dfc(empresa, grupo_dfc)

    if ultimo_ano_dfc:
        st.markdown(
            f"""
            <ul style='
                color: gray;
                font-size: 0.85em;
                padding-left: 18px;
                margin-top: 25px;
                margin-bottom: 0;
            '>
                <li style='margin-bottom: 2px;'>
                    KPI's referentes ao ano mais recente disponível: {ultimo_ano_dfc}.
                </li>
                <li>
                    Valores expressos em R$ mil
                </li>
            </ul>
            """,
            unsafe_allow_html=True
        )

    else:
        st.warning("Nenhum dado disponível para a empresa e grupo selecionados.")


    # Colunas para os cards ficarem lado a lado
    col1, col2, col3, col4, col5, col6 = st.columns(6)

        # Valores inteiros
    v_var_liquida_caixa = var_liquida_caixa(empresa, grupo_dfc)
    v_caixa_operacional = caixa_operacional(empresa, grupo_dfc)
    v_caixa_investimento = caixa_investimento(empresa, grupo_dfc)
    v_caixa_financiamento = caixa_financiamento(empresa, grupo_dfc)
    v_var_cambial_equiv = var_cambial_equiv(empresa, grupo_dfc)
    v_fluxo_caixa_livre = v_caixa_operacional - (valor_capex(empresa, grupo_dfc)*-1)


    # Formata o número no padrão brasileiro
    valor_formatado1 = format_brl(v_var_liquida_caixa)
    valor_formatado2 = format_brl(v_caixa_operacional)
    valor_formatado3 = format_brl(v_caixa_investimento)
    valor_formatado4 = format_brl(v_caixa_financiamento)
    valor_formatado5 = format_brl(v_var_cambial_equiv)
    valor_formatado6 = format_brl(v_fluxo_caixa_livre)

    # KPI's percentuais
    # perc_mg_bruta = (v_mg_bruta / v_receita) * 100 if v_receita else 0
    # perc_ebitda = (v_ebitda / v_receita) * 100 if v_receita else 0
    # perc_lucro_liquido = (v_lucro_liquido / v_receita) * 100 if v_receita else 0

    
    with col1:
        kpi_card("Variação de Caixa", valor_formatado1)
    with col2:
        kpi_card("Operacional", valor_formatado2)
    with col3:
        kpi_card("Investimento", valor_formatado3)
    with col4:
        kpi_card("Financiamento", valor_formatado4)
    with col5:
        kpi_card("Variação Cambial", valor_formatado5)
    with col6:
        kpi_card("Cx Livre (Op - Capex)", valor_formatado6)

    # ====================================
    # Gráficos de Linha
    # ====================================     
    
    # Colunas para os gráficos ficarem lado a lado

    df = get_kpis_dfc_todos_os_anos(empresa, grupo_dfc)

    df_plot = (
        df.pivot(
            index="ANO",
            columns="CD_CONTA",
            values="VL_CONTA"
        )
        .reset_index()
    )

    line_chart(
        df=df_plot,
        col_x="ANO",
        series=[
            {"col": "6.01", "label": "Cx Operacional"},
            {"col": "6.02", "label": "Cx Investimento"},
            {"col": "6.03", "label": "Cx Financiamento"},
            {"col": "6.04", "label": "Var Cambial"},
            {"col": "6.05", "label": "Var Liq."}
        ],
        titulo="Evolução de Caixa x Ano",
        formato_y="numero",
    )

    # ====================================
    # Tabela completa DFC
    # ====================================    

    st.subheader("📈 Análise Horizontal DFC")

    df = get_analise_horizontal_dfc(empresa, grupo_dfc)

    st.markdown(
    """
    <p style='text-align: right;
    color: gray;
    font-size: 0.85em;'>
    Valores expressos em R$ mil
    </p>
    """,
    unsafe_allow_html=True
    )

    df_fmt = formatar_brl_tabela(df)

    st.dataframe(
        formatar_variacao(df_fmt),
        use_container_width=True,
        hide_index=True
    )



# ====================================
# BP
# ====================================

elif pagina == "Balanço Patrimonial":

    st.title("🏦 Balanço Patrimonial")
    
    st.markdown(
    """
    <p style='text-align: left;
    color: red;
    font-size: 1,5em;'>
    RELATÓRIO EM CONSTRUÇÃO.
    </p>
    """,
    unsafe_allow_html=True
    )


    grupos_df = get_grupos_bp(empresa)

    grupo_bp = st.selectbox(
        "Grupo e método do balanço patrimonial",
        grupos_df["GRUPO_DFP"]
    )