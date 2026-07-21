import pandas as pd
from pathlib import Path
import os
import time
import sqlite3
from src.validator import validador_df_bp


# Diretórios para os arquivos
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / 'data' / 'raw'
CLEAN_DIR = BASE_DIR / 'data' / 'clean'
CLEAN_DIR.mkdir(parents=True, exist_ok=True) 
CHECK_DIR = BASE_DIR / 'data' / 'check'
CHECK_DIR.mkdir(parents=True, exist_ok=True) 
DB_DIR = BASE_DIR / 'data' / 'db'
DB_DIR.mkdir(parents=True, exist_ok=True)



# Unificar as bases de dados em um único DataFrame de acordo com os tipos de arquivos (DFC, DRE, BPA, BPP e etc)

def unificar_bases_bp(RAW_DIR: str) -> pd.DataFrame:
    '''Unifica os arquivos de Balanço Patrimonial em um único DataFrame.'''

    df_bp = []

    for file in os.listdir(RAW_DIR):
        if "BP" in file:
            file_path = os.path.join(RAW_DIR, file)
            df_temp = pd.read_csv(file_path, encoding='latin1', sep=';', low_memory=False)
            print(f"{file} -> {len(df_temp)} linhas") # ponto de conferência
            df_bp.append(df_temp)


    df_bp_final =pd.concat(df_bp, ignore_index=True)
    
    print(f' Total de linhas no final: {len(df_bp_final)}')

    return df_bp_final

    # =========================
    # TRATAMENTOS
    # =========================

def transformar_bp(df: pd.DataFrame) -> pd.DataFrame:
    '''Realiza os tratamentos necessários'''

    # converter para data
    date_cols = ['DT_REFER', 'DT_FIM_EXERC']

    for col in date_cols:
        df[col] = pd.to_datetime(
            df[col],
            errors='coerce'
        ).dt.date  
    
    
    # extrair ano da coluna de data
    df['ANO'] = pd.to_datetime(
        df['DT_FIM_EXERC'],
        errors='coerce'
    ).dt.year.astype('Int64')

    # substituir NaN por None
    df = df.astype(object).where(
        pd.notnull(df),
        None
    )

    # filtrar somente última versão
    df = df[df['ORDEM_EXERC'] == 'ÚLTIMO']


    # tratando duplicidades
    colunas_chave = ['CNPJ_CIA', 'CD_CVM', 'GRUPO_DFP', 'CD_CONTA', 'ANO']

    duplicados = df.duplicated(subset=colunas_chave, keep=False)
    if duplicados.any():
        print(f"[WARN] {duplicados.sum()} linhas duplicadas encontradas no arquivo BP — mantendo primeira ocorrência.")

    df = df.drop_duplicates(subset=colunas_chave, keep='first')

    return df



    # =========================
    # VALIDAÇÃO
    # =========================

def validar_bp(df: pd.DataFrame):
    '''Valida os dados e salva erros'''

    valid_rows, errors = validador_df_bp(df)

    print(f'Linhas válidas: {len(valid_rows)}')
    print(f'Erros encontrados: {len(errors)}')

    # salvar erros e avisar usuário
    df_errors = pd.DataFrame(errors)
    df_errors.to_csv(CHECK_DIR / "bp_errors.csv", index=False)
    
    if errors:
        print("\n⚠️  inconsistências encontradas, favor analisar arquivo na pasta check.")
    else:
        print("\n ✅  Nenhum erro encontrado na validação.")

    return valid_rows, errors
    

# =========================
# SALVAMENTO CSV CLEAN
# =========================

def salvar_bp(df: pd.DataFrame) -> None:
    '''Salva o DataFrame final em um arquivo CSV.'''

    # salva depois de terminar a concatenação
    df.to_csv(
        CLEAN_DIR / 'BP_unificado.csv',
        index=False,
        encoding='latin1',
        sep=';'
    )



# # ---------------testes---------------




