import streamlit as st

from src.utils.components import kpi_card
from src.utils.formatters import (
    formatar_brl_tabela_DRE,
    format_brl
)
from src.queries_dre import (
    get_empresas,
    get_grupos,
    get_dre_empresa,
    get_receita_card,
    ano_mais_recente,
    get_mg_bruta_card,
    get_ebit_card,
    get_ebitda_card,
    get_lucro_liquido
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
grupos_df = get_grupos()

empresa = st.sidebar.selectbox(
    "Empresa",
    empresas_df["DENOM_CIA"]
)

grupo = st.sidebar.selectbox(
    "Grupo",
    grupos_df["GRUPO_DFP"]
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

    # ====================================
    # CARDS TOPO PÁGINA
    # ====================================  
    
    ultimo_ano = ano_mais_recente(empresa, grupo)

    if ultimo_ano:
        st.markdown(
        f"""
        <p style='text-align: left;
        color: gray;
        font-size: 0.85em;'>
        KPI's referentes ao ano mais recente disponível: {ultimo_ano}.
        </p>
        """,
        unsafe_allow_html=True
        )
    else:
        st.warning("Nenhum dado disponível para a empresa e grupo selecionados.")



    # KPI's cards
    col1, col2, col3, col4 = st.columns(4)
    
    # Valores inteiros
    v_receita = get_receita_card(empresa, grupo)
    v_mg_bruta = get_mg_bruta_card(empresa, grupo)
    v_ebit = get_ebit_card(empresa, grupo)
    v_ebitda = get_ebitda_card(empresa, grupo)
    v_ebitda = v_ebit + v_ebitda
    v_lucro_liquido = get_lucro_liquido(empresa, grupo)

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

   
    
    df = get_dre_empresa(empresa, grupo)

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

    st.dataframe(
        formatar_brl_tabela_DRE(df),
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

    st.write(f"Empresa selecionada: {empresa}")
    st.write(f"Grupo selecionado: {grupo}")

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
    st.write(f"Grupo selecionado: {grupo}")