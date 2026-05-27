import streamlit as st


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
                font-size: 26px;
                font-weight: 700;
            ">
                {valor}
            </h2>

            {variacao_html}
        </div>
    </div>
    """)