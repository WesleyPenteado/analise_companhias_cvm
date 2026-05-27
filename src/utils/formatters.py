import pandas as pd

def format_brl(valor):
    return f"R$ {valor:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_brl_tabela_DRE(df):
    colunas_valor = ["Ano_2025", "Ano_2024", "Ano_2023", "Ano_2022", "Ano_2021"]
    df_fmt = df.copy()
    for col in colunas_valor:
        if col in df_fmt.columns:
            df_fmt[col] = df_fmt[col].apply(
                lambda x: f"{x:_.0f}".replace(".", ",").replace("_", ".") if pd.notna(x) else ""
            )
    return df_fmt