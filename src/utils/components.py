import streamlit as st
import plotly.graph_objects as go
import pandas as pd


# ====================================
# Informação de texto customizada
# ====================================
def custom_info(texto, cor_fundo="#e8f4fd", cor_texto="#0c5480", cor_borda="#0c5480"):
    '''Exibe uma caixa de informação customizada com cores e estilo definidos.'''
    st.markdown(
        f"""
        <div style="
            background-color: {cor_fundo};
            color: {cor_texto};
            border-left: 4px solid {cor_borda};
            padding: 12px 16px;
            border-radius: 4px;
            margin-bottom: 0px;
        ">
            {texto}
        </div>
        """,
        unsafe_allow_html=True
    )


# ====================================
# CARDS
# ====================================
def kpi_card(titulo, valor, percentual=None, label_percentual=None, maior_melhor=True):
    '''Cria um card de KPI com título, valor e percentual de variação ou kpi opcional.
    
    label_percentual: texto opcional exibido antes do percentual, ex: "YoY", "vs. ano anterior"

    '''

    percentual_html = ""

    if percentual is not None:

        if maior_melhor:
            positivo = percentual >= 0
        else:
            positivo = percentual <= 0

        cor = "#10B981" if positivo else "#EF4444"

        label_html = ""
        if label_percentual:
            label_html = f"""
            <span style="
                font-size: 12px;
                color: #6B7280;
                font-weight: 500;
                margin-right: 4px;
            ">
                {label_percentual}
            </span>
            """
        percentual_html = f"""
        {label_html}
        <span style="
            font-size: 14px;
            color: {cor};
            font-weight: 600;
        ">
            {percentual:.1f}%
        </span>
        """

    st.html(f"""
    <div style="
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    ">
        <p style="
            color: #6B7280;
            font-size: 14px;
            margin: 0 0 8px 0;
        ">
            {titulo}
        </p>

        <div style="
            display: flex;
            align-items: baseline;
            gap: 8px;
        ">
            <h2 style="
                color: #111827;
                margin: 0;
                font-size: 20px;
                font-weight: 700;
            ">
                {valor}
            </h2>

            {percentual_html}
        </div>
    </div>
    """)


# ====================================
# GRÁFICO DE LINHA
# ====================================


# Paleta de azuis alinhada com o visual dos cards
_LINE_COLORS = [
    "#636EFA",
    "#EF553B",
    "#00CC96",
    "#AB63FA",
    "#FFA15A",
]

def line_chart(
    df: pd.DataFrame,
    col_x: str,
    series: list[dict],
    titulo: str = "",
    formato_y: str = "monetario",  # "monetario" | "numero" | "percentual"
    altura: int = 360,
):
    """
    Gráfico de linha reutilizável com até 5 séries.

    Parâmetros
    ----------
    df        : DataFrame com os dados já agregados
    col_x     : Nome da coluna que será o eixo X (ex: "ANO")
    series    : Lista de dicts com {"col": <coluna_y>, "label": <nome_legenda>}
                Exemplo: [{"col": "RECEITA", "label": "Receita Líquida"},
                          {"col": "CUSTO",   "label": "Custo"}]
    titulo    : Título exibido no topo do card
    formato_y : Formatação dos rótulos do eixo Y
    altura    : Altura do gráfico em pixels
    """

    # --- Validação ---------------------------------------------------------
    if len(series) > 5:
        raise ValueError("A função suporta no máximo 5 séries.")

    # --- Formatação do eixo Y ----------------------------------------------
    _formatos = {
        "monetario":   {"tickprefix": "R$ ", "tickformat": ",.0f"},
        "numero":      {"tickprefix": "",    "tickformat": ",.0f"},
        "percentual":  {"tickprefix": "",    "tickformat": ".1f", "ticksuffix": "%"},
    }
    fmt = _formatos.get(formato_y, _formatos["numero"])

    # --- Construção das traces ---------------------------------------------
    fig = go.Figure()

    for i, serie in enumerate(series):
        cor = _LINE_COLORS[i]

        fig.add_trace(go.Scatter(
            x=df[col_x],
            y=df[serie["col"]],
            name=serie["label"],
            mode="lines+markers",
            line=dict(color=cor, width=2.5),
            marker=dict(color=cor, size=7, line=dict(color="#FFFFFF", width=1.5)),
            hovertemplate=(
                f"<b>{serie['label']}</b><br>"
                f"{col_x}: %{{x}}<br>"
                f"Valor: %{{y:{fmt['tickformat']}}}<extra></extra>"
            ),
        ))

    # --- Layout no formato padrão da página -------------------------------
    fig.update_layout(
        title=dict(
            text=titulo,
            font=dict(size=15, color="#111827", family="sans-serif"),
            x=0,
            pad=dict(l=4),
        ),
        showlegend=len(series) > 1,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        height=altura,
        margin=dict(l=16, r=16, t=48 if titulo else 16, b=16),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="left",
            x=0,
            font=dict(color="#6B7280", size=12),
        ),
        xaxis=dict(
            type="category",
            tickfont=dict(color="#6B7280", size=12),
            gridcolor="#F3F4F6",
            linecolor="#E5E7EB",
            showline=True,
        ),
        yaxis=dict(
            tickfont=dict(color="#6B7280", size=12),
            gridcolor="#F3F4F6",
            linecolor="#E5E7EB",
            showline=True,
            **fmt,
        ),
        hovermode="x unified",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ====================================
# PREPARAÇÃO DE DADOS - WATERFALL
# ====================================

MAPA_DFC_WATERFALL = {
    '6.05.01': 'Caixa Inicial',
    '6.01':    'Var. Operacional',
    '6.02':    'Var. Investimentos',
    '6.03':    'Var. Financiamento',
    '6.04':    'Var. Cambial',
    '6.05.02': 'Caixa Final',
}

def preparar_dados_waterfall(
    df_raw: pd.DataFrame,
    mapa_categorias: dict,
    col_conta: str = "CD_CONTA",
    col_valor: str = "VL_CONTA",
    categorias_absolutas: tuple = ("Caixa Inicial", "Caixa Final"),
    calcular_final_automaticamente: bool = True,
) -> pd.DataFrame:
    """
    Transforma um DataFrame "cru" (linhas por conta) em um DataFrame
    pronto para o waterfall_chart, com colunas: categoria, valor, measure.

    Parâmetros
    ----------
    df_raw                  : DataFrame vindo da query (ex: DFC)
    mapa_categorias         : dict {codigo_conta: nome_categoria}, na ORDEM desejada
    col_conta                : nome da coluna de código da conta
    col_valor                 : nome da coluna de valor
    categorias_absolutas    : quais categorias são "totais" (barra do zero)
    calcular_final_automaticamente : se True, recalcula a última categoria
                                       absoluta somando as relativas, ao invés
                                       de confiar no valor bruto do banco
    """
    ordem = list(mapa_categorias.values())

    df = df_raw.copy()
    df["categoria"] = df[col_conta].map(mapa_categorias)
    df = df.dropna(subset=["categoria"])

    # garante todas as categorias presentes, na ordem certa
    df = (
        df.set_index("categoria")
        .reindex(ordem)
        .reset_index()
    )
    df[col_valor] = df[col_valor].fillna(0.0).astype(float)

    df["measure"] = df["categoria"].apply(
        lambda c: "absolute" if c in categorias_absolutas else "relative"
    )

    df = df.rename(columns={col_valor: "valor"})[["categoria", "valor", "measure"]]

    if calcular_final_automaticamente and len(categorias_absolutas) >= 1:
        # recalcula a última categoria absoluta como soma acumulada
        ultima_abs = [c for c in ordem if c in categorias_absolutas][-1]
        idx_ultima = df.index[df["categoria"] == ultima_abs][0]
        soma_ate_aqui = df.loc[: idx_ultima - 1, "valor"].sum()
        df.loc[idx_ultima, "valor"] = soma_ate_aqui

    return df

# ====================================
# GRÁFICO DE CASCATA (WATERFALL)
# ====================================

def waterfall_chart(
    df: pd.DataFrame,
    col_categoria: str = "categoria",
    col_valor: str = "valor",
    col_measure: str = "measure",
    titulo: str = "",
    formato_y: str = "monetario",  # "monetario" | "numero" | "percentual"
    altura: int = 400,
    mostrar_totais_em_azul: bool = True,
):
    """
    Gráfico de cascata (waterfall) reutilizável, no padrão visual dos demais
    componentes da página.

    df deve conter as colunas:
        - col_categoria : rótulo de cada barra (ex: "Caixa Inicial")
        - col_valor      : valor numérico (positivo ou negativo)
        - col_measure    : "absolute" ou "relative"
    """

    _formatos = {
        "monetario":  {"tickprefix": "R$ ", "tickformat": ",.0f"},
        "numero":     {"tickprefix": "",    "tickformat": ",.0f"},
        "percentual": {"tickprefix": "",    "tickformat": ".1f", "ticksuffix": "%"},
    }
    fmt = _formatos.get(formato_y, _formatos["numero"])

    cor_aumento = "#10B981"   # verde, igual ao kpi_card
    cor_diminuicao = "#EF4444"  # vermelho, igual ao kpi_card
    cor_total = "#636EFA" if mostrar_totais_em_azul else "#6B7280"

    textos = [
        f"{fmt['tickprefix']}{v:,.0f}" for v in df[col_valor]
    ]

    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=df[col_measure],
        x=df[col_categoria],
        y=df[col_valor],
        text=textos,
        textposition="outside",
        textfont=dict(color="#111827", size=12),
        connector={"line": {"color": "#E5E7EB", "width": 1.5}},
        increasing={"marker": {"color": cor_aumento}},
        decreasing={"marker": {"color": cor_diminuicao}},
        totals={"marker": {"color": cor_total}},
        hovertemplate=(
            "<b>%{x}</b><br>"
            f"Valor: %{{y:{fmt['tickformat']}}}<extra></extra>"
        ),
    ))

    fig.update_layout(
        title=dict(
            text=titulo,
            font=dict(size=15, color="#111827", family="sans-serif"),
            x=0,
            pad=dict(l=4),
        ),
        showlegend=False,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        height=altura,
        margin=dict(l=16, r=16, t=48 if titulo else 16, b=16),
        waterfallgap=0.3,
        xaxis=dict(
            type="category",
            tickfont=dict(color="#6B7280", size=12),
            gridcolor="#F3F4F6",
            linecolor="#E5E7EB",
            showline=True,
        ),
        yaxis=dict(
            tickfont=dict(color="#6B7280", size=12),
            gridcolor="#F3F4F6",
            linecolor="#E5E7EB",
            showline=True,
            **fmt,
        ),
    )

    st.plotly_chart(fig, use_container_width=True)