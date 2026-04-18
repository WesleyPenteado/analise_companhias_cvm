import pandas as pd
import RAW_DIR from igestion


# 1. Unificar as bases de dados em um único DataFrame de acordo com os tipos de arquivos (DFC, DRE)
def unificar_bases_dfc_md(RAW_DIR: str) -> pd.DataFrame:
    '''Unifica os arquivos DFC_MD em um único DataFrame.'''
    df_dfc = pd.DataFrame()

    for file in os.listdir(RAW_DIR):
        if "DFC_MD" in file:
            file_path = os.path.join(RAW_DIR, file)
            df_temp = pd.read_csv(file_path, encoding='latin1', sep=';', low_memory=False)
            df_dfc = pd.concat([df_dfc, df_temp], ignore_index=True)

    return df_dfc

