import pandas as pd
from pathlib import Path
import os
import openpyxl
from validator import validate_df_DRE

# Diretórios para os arquivos
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / 'data' / 'raw'
CLEAN_DIR = BASE_DIR / 'data' / 'clean'
CLEAN_DIR.mkdir(parents=True, exist_ok=True) 
CHECK_DIR = BASE_DIR / 'data' / 'check'
CHECK_DIR.mkdir(parents=True, exist_ok=True) 


# Unificar as bases de dados em um único DataFrame de acordo com os tipos de arquivos (DFC, DRE, BPA, BPP e etc)

def unificar_bases_dre_con(RAW_DIR: str) -> pd.DataFrame:
    '''Unifica os arquivos DRE_consolidada em um único DataFrame.'''

    df_DRE_con = []

    for file in os.listdir(RAW_DIR):
        if "DRE_con" in file:
            file_path = os.path.join(RAW_DIR, file)
            df_temp = pd.read_csv(file_path, encoding='latin1', sep=';', low_memory=False)
            print(f"{file} -> {len(df_temp)} linhas") # ponto de conferência
            df_DRE_con.append(df_temp)

    df_DRE_con_final = pd.concat(df_DRE_con, ignore_index=True)
    print(f' Total de linhas no final: {len(df_DRE_con_final)}')

    # converter para data
    df_DRE_con_final['DT_REFER'] = pd.to_datetime(
        df_DRE_con_final['DT_REFER'], errors='coerce'
    )

    # extrair ano da coluna de data
    df_DRE_con_final['ANO'] = df_DRE_con_final['DT_REFER'].dt.year.astype('Int64')

    # validar o DataFrame
    valid_rows, errors = validate_df_DRE(df_DRE_con_final)
    print(f'Linhas válidas: {len(valid_rows)}')
    print(f'Erros encontrados: {len(errors)}')

    # salvar erros e avisar usuário
    df_errors = pd.DataFrame(errors)
    df_errors.to_csv(CHECK_DIR / "dre_errors.csv", index=False)
    
    if errors:
        print("\n⚠️  inconsistências encontradas, favor analisar arquivo na pasta check.")
    else:
        print("\n ✅  Nenhum erro encontrado na validação.")
    

    # salva depois de terminar a concatenação
    df_DRE_con_final.to_csv(
        CLEAN_DIR / 'DRE_con_unificado.csv',
        index=False,
        encoding='latin1',
        sep=';'
    )

    return df_DRE_con_final









# # ---------------testes---------------
if __name__ == "__main__":

    df = unificar_bases_dre_con(RAW_DIR)

    # df = pd.read_csv(CLEAN_DIR / 'DRE_con_unificado.csv', encoding='latin1', sep=';')

#     df.to_excel(
#         CHECK_DIR / 'DRE_con_unificado.xlsx',
#         index=False,
#         engine='openpyxl',
#     )