import streamlit as st
import plotly.graph_objects as go
import pandas as pd



# ====================================
# CARDS
# ====================================
def kpi_card(titulo, valor, variacao=None):
    '''Cria um card de KPI com título, valor e variação percentual opcional.'''

    variacao_html = ""

    if variacao is not None:
        cor = "#10B981" if variacao >= 0 else "#EF4444"
        sinal = "+" if variacao > 0 else ""

        variacao_html = f"""
        <span style="
            font-size: 14px;
            color: {cor};
            font-weight: 600;
        ">
            {sinal}{variacao:.1f}%
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

            {variacao_html}
        </div>
    </div>
    """)


# ====================================
# GRÁFICO DE LINHA
# ====================================


# Paleta de azuis alinhada com o visual dos cards
_LINE_COLORS = ["#1D4ED8", "#60A5FA", "#93C5FD"]

def line_chart(
    df: pd.DataFrame,
    col_x: str,
    series: list[dict],
    titulo: str = "",
    formato_y: str = "monetario",  # "monetario" | "numero" | "percentual"
    altura: int = 360,
):
    """
    Gráfico de linha reutilizável com até 3 séries.

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
    if len(series) > 3:
        raise ValueError("A função suporta no máximo 3 séries.")

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