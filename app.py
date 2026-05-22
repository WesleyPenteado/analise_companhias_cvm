import streamlit as st

from src.dashboard_dre import (
    get_empresas,
    get_grupos,
    get_dre_empresa,
    formatar_brl,
    get_receita_card,
    ano_mais_recente,
    get_mg_bruta_card
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

    st.title("📊 DRE Dashboard - CVM")

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


    col1, col2, col3, col4 = st.columns(4)
    
    valor1 = get_receita_card(empresa, grupo)
    valor2 = get_mg_bruta_card(empresa, grupo)

    # Formata o número no padrão brasileiro
    valor_formatado1 = f"R$ {valor1:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    valor_formatado2 = f"R$ {valor2:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")


    
    with col1:
        st.html(f"""
        <div style="
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #E5E7EB;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        ">
            <p style="color: #6B7280; font-size: 14px; margin: 0 0 8px 0;">
                Receita Líquida
            </p>
            <h2 style="color: #111827; margin: 0; font-size: 32px; font-weight: 700;">
                {valor_formatado1}
            </h2>
        </div>
        """)

    with col2:
        st.html(f"""
        <div style="
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #E5E7EB;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        ">
            <p style="color: #6B7280; font-size: 14px; margin: 0 0 8px 0;">
                Margem Bruta
            </p>
            <h2 style="color: #111827; margin: 0; font-size: 32px; font-weight: 700;">
                {valor_formatado2}
            </h2>
        </div>
        """)
    
    
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
        formatar_brl(df),
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