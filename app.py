import streamlit as st

from src.utils.components import (
    custom_info,
    kpi_card,
    line_chart,
    preparar_dados_waterfall,
    waterfall_chart,
    MAPA_DFC_WATERFALL,
    stacked_bar_chart_grouped
)
from src.utils.formatters import (
    formatar_brl_tabela,
    format_brl,
    format_percentual,
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
    var_liquida_caixa_penultimo_ano,
    caixa_operacional,
    caixa_operacional_penultimo_ano,
    valor_capex,
    valor_capex_penultimo_ano,
    get_kpis_dfc_todos_os_anos,
    get_analise_horizontal_dfc,
    get_waterfall_último_ano
)

from src.queries_bp import (
    get_grupos_bp,
    ano_mais_recente_bp,
    tipo_bp,
    ativo_circulante_ou_caixa,
    passivo_circulante_ou_financeiro,
    ativo_estoques,
    passivo_nao_circulante,
    patrimonio_liquido,
    ativo_total,
    kpis_evolucao_ativo_passivo_pl
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
                    Valores expressos em R$ mil quando moeda
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
        kpi_card("Margem Bruta", valor_formatado2, perc_mg_bruta, maior_melhor=True)
 
    with col3:
        kpi_card("EBITDA", valor_formatado3, perc_ebitda, maior_melhor=True)

    with col4:
        kpi_card("Lucro Líquido", valor_formatado4, perc_lucro_liquido, maior_melhor=True)

    

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

    grupos_df = get_grupos_dfc(empresa)

    grupo_dfc = st.selectbox(
        "Grupo e método do fluxo de caixa",
        grupos_df["GRUPO_DFP"]
    )

    
    ultimo_ano_dfc = ano_mais_recente_dfc(empresa, grupo_dfc)
    penultimo_ano_dfc = ultimo_ano_dfc - 1 if ultimo_ano_dfc else None

    # ====================================
    # CARDS TOPO PÁGINA
    # ====================================  


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
                    Valores expressos em R$ mil quando moeda
                </li>
            </ul>
            """,
            unsafe_allow_html=True
        )

    else:
        st.warning("Nenhum dado disponível para a empresa e grupo selecionados.")


    # Colunas para os cards ficarem lado a lado
    col1, col2 = st.columns(2)

        # Valores inteiros
    v_var_liq_caixa = var_liquida_caixa(empresa, grupo_dfc)
    v_var_liq_caixa_penultimo_ano = var_liquida_caixa_penultimo_ano(empresa, grupo_dfc)
    v_caixa_operacional = caixa_operacional(empresa, grupo_dfc)
    v_fluxo_caixa_livre = v_caixa_operacional - (valor_capex(empresa, grupo_dfc)*-1)
    v_caixa_operacional_penultimo_ano = caixa_operacional_penultimo_ano(empresa, grupo_dfc, penultimo_ano_dfc)
    v_fluxo_caixa_livre_penultimo_ano = v_caixa_operacional_penultimo_ano - (valor_capex_penultimo_ano(empresa, grupo_dfc, penultimo_ano_dfc)*-1)



    # Formata o número no padrão brasileiro
    valor_formatado1 = format_brl(v_var_liq_caixa)
    valor_formatado2 = format_brl(v_fluxo_caixa_livre)
    valor_formatado3 = format_brl(v_var_liq_caixa_penultimo_ano)
    valor_formatado4 = format_brl(v_fluxo_caixa_livre_penultimo_ano)

    # KPI's percentuais
    perc_yoy_var_liq_caixa = ((v_var_liq_caixa - v_var_liq_caixa_penultimo_ano) / v_var_liq_caixa_penultimo_ano * 100 
                                   if v_var_liq_caixa_penultimo_ano else 0)

    perc_yoy_fluxo_caixa_livre = ((v_fluxo_caixa_livre - v_fluxo_caixa_livre_penultimo_ano) / v_fluxo_caixa_livre_penultimo_ano * 100
                                   if v_fluxo_caixa_livre_penultimo_ano else 0)
    
    with col1:
        kpi_card("Variação de Caixa", valor_formatado1, perc_yoy_var_liq_caixa, label_percentual="YoY", maior_melhor=True)
    with col2:
        kpi_card("Fluxo de Caixa Livre (Operacional - CAPEX)", valor_formatado2, perc_yoy_fluxo_caixa_livre, label_percentual="YoY", maior_melhor=True)


    # ====================================
    # Gráficos Waterfall
    # ====================================    

    df_raw = get_waterfall_último_ano(empresa, grupo_dfc, ultimo_ano_dfc)

    if not df_raw.empty:
        df_wf = preparar_dados_waterfall(df_raw, MAPA_DFC_WATERFALL)
        waterfall_chart(df_wf, titulo=f"Fluxo de Caixa {ultimo_ano_dfc}", formato_y="monetario")



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
            {"col": "6.05", "label": "Variação Líquida"}
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


    grupo_bp = get_grupos_bp(empresa)

    grupo_bp = st.selectbox(
        "Grupo e método do balanço patrimonial",
        grupo_bp["GRUPO_DFP"]
    )

    ultimo_ano_bp = ano_mais_recente_bp(empresa, grupo_bp)
    penultimo_ano_bp = ultimo_ano_bp - 1 if ultimo_ano_bp else None

    tipo_bp_value = tipo_bp(empresa, grupo_bp, ultimo_ano_bp)

    if tipo_bp_value == "Instituição Não Financeira":
        custom_info("<b>Instituição Não Financeira</b>: será exibido relatório padrão de balanço patrimonial")

        # ====================================
        # CARDS TOPO PÁGINA
        # ====================================  


        if ultimo_ano_bp:
            st.markdown(
                f"""
                <ul style='
                    color: gray;
                    font-size: 0.85em;
                    padding-left: 18px;
                    margin-top: 5px;
                    margin-bottom: 25px;
                '>
                    <li style='margin-bottom: 2px;'>
                        KPI's referentes ao ano mais recente disponível: {ultimo_ano_bp}.
                    </li>
                    <li>
                        Valores expressos em R$ mil quando moeda
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
        a_circulante_101 = ativo_circulante_ou_caixa(empresa, grupo_bp, ultimo_ano_bp)
        p_circulante_201 = passivo_circulante_ou_financeiro(empresa, grupo_bp, ultimo_ano_bp)
        a_circulante_101_penultimo = ativo_circulante_ou_caixa(empresa, grupo_bp, penultimo_ano_bp)
        p_circulante_201_penultimo = passivo_circulante_ou_financeiro(empresa, grupo_bp, penultimo_ano_bp)
        a_estoques = ativo_estoques(empresa, grupo_bp, ultimo_ano_bp)
        a_estoques_penultimo = ativo_estoques(empresa, grupo_bp, penultimo_ano_bp)
        p_nao_circulante202 = passivo_nao_circulante(empresa, grupo_bp, ultimo_ano_bp)
        p_nao_circulante202_penultimo = passivo_nao_circulante(empresa, grupo_bp, penultimo_ano_bp)
        p_patrimonio_liquido203 = patrimonio_liquido(empresa, grupo_bp, ultimo_ano_bp)
        p_patrimonio_liquido203_penultimo = patrimonio_liquido(empresa, grupo_bp, penultimo_ano_bp)
        a_total = ativo_total(empresa, grupo_bp, ultimo_ano_bp)
        a_total_penultimo = ativo_total(empresa, grupo_bp, penultimo_ano_bp)
     

        # Cálculo KPI's liquidez
        liq_corrente = round((a_circulante_101 / p_circulante_201) if p_circulante_201 else 0, 2)
        liq_corrente_penultimo = round((a_circulante_101_penultimo / p_circulante_201_penultimo) if p_circulante_201_penultimo else 0, 2)
        perc_yoy_liq_corrente = ((liq_corrente - liq_corrente_penultimo) / liq_corrente_penultimo * 100) if liq_corrente_penultimo else 0

        liq_seca = round(((a_circulante_101 - a_estoques) / p_circulante_201) if p_circulante_201 else 0, 2)
        liq_seca_penultimo = round(((a_circulante_101_penultimo - a_estoques_penultimo) / p_circulante_201_penultimo) if p_circulante_201_penultimo else 0, 2)
        perc_yoy_liq_seca = ((liq_seca - liq_seca_penultimo) / liq_seca_penultimo * 100) if liq_seca_penultimo else 0

        # Cálculo KPI's endividamento: grau de dependência do capital de terceiros em relação ao capital próprio.
        endividamento = (p_circulante_201 + p_nao_circulante202) / p_patrimonio_liquido203 * 100 if p_patrimonio_liquido203 else 0
        endividamento_penultimo = ((p_circulante_201_penultimo + p_nao_circulante202_penultimo) / p_patrimonio_liquido203_penultimo * 100) if p_patrimonio_liquido203_penultimo else 0
        perc_yoy_endividamento = ((endividamento - endividamento_penultimo) / endividamento_penultimo * 100) if endividamento_penultimo else 0

         # Capitalização ou alavancagem financeira: proporção do ativo financiada com capital próprio.
        capitalizacao = round(p_patrimonio_liquido203 / a_total * 100 if a_total else 0, 2)
        capitalizacao_penultimo = round((p_patrimonio_liquido203_penultimo / a_total_penultimo * 100) if a_total_penultimo else 0, 2)
        perc_yoy_capitalizacao = ((capitalizacao - capitalizacao_penultimo) / capitalizacao_penultimo * 100) if capitalizacao_penultimo else 0

        
        with col1:
            kpi_card("Liq. Corrente", liq_corrente, perc_yoy_liq_corrente, label_percentual="YoY", maior_melhor=True)
        with col2:
            kpi_card("Liq. Seca", liq_seca, perc_yoy_liq_seca, label_percentual="YoY", maior_melhor=True)
        with col3:
            kpi_card("Particip. Cap. 3º", format_percentual(endividamento), perc_yoy_endividamento, label_percentual="YoY", maior_melhor=False)
        with col4:
            kpi_card("Grau de capitalização", format_percentual(capitalizacao), perc_yoy_capitalizacao, label_percentual="YoY", maior_melhor=True)



        # ====================================
        # Gráficos de colunas empilhadas e agrupadas (Ativo vs Passivo + PL por ano)
        # ====================================  
        
        _MAPA_CONTAS = {
            "1.01": "Ativo Circulante",
            "1.02": "Ativo Não Circulante",
            "2.01": "Passivo Circulante",
            "2.02": "Passivo Não Circulante",
            "2.03": "Patrimônio Líquido",
        }

        _MAPA_GRUPO = {
            "1.01": "Ativo",
            "1.02": "Ativo",
            "2.01": "Passivo + PL",
            "2.02": "Passivo + PL",
            "2.03": "Passivo + PL",
        }

        df = kpis_evolucao_ativo_passivo_pl(empresa, grupo_bp)
        df["CONTA"] = df["CD_CONTA"].map(_MAPA_CONTAS)
        df["GRUPO"] = df["CD_CONTA"].map(_MAPA_GRUPO)

        stacked_bar_chart_grouped(
            df=df,
            col_x="ANO",
            col_grupo="GRUPO",
            col_conta="CONTA",
            col_valor="VL_CONTA",
            contas=[
                {"col": "Ativo Não Circulante", "label": "Ativo Não Circulante"},
                {"col": "Ativo Circulante", "label": "Ativo Circulante"},
                {"col": "Patrimônio Líquido", "label": "Patrimônio Líquido"},                
                {"col": "Passivo Não Circulante", "label": "Passivo Não Circulante"},
                {"col": "Passivo Circulante", "label": "Passivo Circulante"},
            ],
            titulo="Evolução do Balanço Patrimonial: Ativo vs. Passivo + PL",
            formato_y="monetario",
        )

    else:
        custom_info(
            "<b>Instituição Financeira</b>: executada análise específica para este modelo de empresa",
            cor_fundo="#fff8e1",
            cor_texto="#7a5c00",
            cor_borda="#f0b400"
        )
