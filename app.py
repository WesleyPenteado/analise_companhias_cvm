import streamlit as st

from src.utils.components import (
    kpi_card,
    line_chart
)
from src.utils.formatters import (
    formatar_brl_tabela_DRE,
    format_brl,
    formatar_variacao_dre
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
    ano_mais_recente_dfc
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

st.sidebar.title("📁 Navegação")

empresas_df = get_empresas()
grupos_df = get_grupos_dre()

empresa = st.sidebar.selectbox(
    "Escolha a empresa",
    empresas_df["DENOM_CIA"]
)



st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "Selecione a análise:",
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

    df_fmt = formatar_brl_tabela_DRE(df)

    st.dataframe(
        formatar_variacao_dre(df_fmt),
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

    df_fmt = formatar_brl_tabela_DRE(df)

    st.dataframe(
        formatar_variacao_dre(df_fmt),
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

    grupos_df = get_grupos_dfc()

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

    st.write(f"Empresa selecionada: {empresa}")
    st.write(f"Grupo selecionado: {grupo_dre}")