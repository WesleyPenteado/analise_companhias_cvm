import pandas as pd
from pathlib import Path
import os

# Criando caminhos para os arquivos
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / 'data' / 'raw'
CLEAN_DIR = BASE_DIR / 'data' / 'clean'


# Unificar as bases de dados em um único DataFrame de acordo com os tipos de arquivos (DFC, DRE)
def unificar_bases_dfc_md_con(RAW_DIR: str) -> pd.DataFrame:
    '''Unifica os arquivos DFC_MD em um único DataFrame.'''
    df_dfc_md_con = pd.DataFrame()

    df_dfc_md_con = []

    for file in os.listdir(RAW_DIR):
        if "DFC_MD_con" in file:
            file_path = os.path.join(RAW_DIR, file)
            df_temp = pd.read_csv(file_path, encoding='latin1', sep=';', low_memory=False)
            print(f"{file} -> {len(df_temp)} linhas") # ponto de conferência
            df_dfc_md_con.append(df_temp)

    df_dfc_md_con_final = pd.concat(df_dfc_md_con, ignore_index=True)

    # salva depois de terminar a concatenação
    df_dfc_md_con_final.to_csv(
        CLEAN_DIR / 'dfc_md_con_unificado.csv',
        index=False,
        encoding='latin1',
        sep=';'
    )

    return df_dfc_md_con

if __name__ == "__main__":

    df = pd.read_csv(CLEAN_DIR / 'dfc_md_con_unificado.csv', encoding='latin1', sep=';')

    print(df.sample(10))