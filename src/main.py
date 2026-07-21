from src.ingestion import get_available_years, download_and_extract
from src.transformation_dre import unificar_bases_dre, transformar_dre, validar_dre, salvar_dre, limpar_todos_csvs_raw
from src.transformation_dfc import unificar_bases_dfc, transformar_dfc, validar_dfc, salvar_dfc
from src.transformation_bp import unificar_bases_bp, transformar_bp, validar_bp, salvar_bp
from src.load import load_dre_to_db, load_dfc_to_db, load_bp_to_db
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / 'data' / 'raw'
RAW_DIR.mkdir(parents=True, exist_ok=True)
CLEAN_DIR = BASE_DIR / 'data' / 'clean'
CLEAN_DIR.mkdir(parents=True, exist_ok=True)

def main():
    print("🔎 Buscando anos disponíveis...")
    anos = get_available_years()
    
    print(f"📅 Anos encontrados: {anos}")

    for ano in anos:
        download_and_extract(ano, str(RAW_DIR))
    print("✅ Download e extração concluídos!")

    print("Iniciando processamento dos dados...")
    
    # Processando DRE
    df_dre = unificar_bases_dre(RAW_DIR)
    df_dre = transformar_dre(df_dre)
    valid_rows, errors = validar_dre(df_dre)

    if not errors:
        salvar_dre(df_dre)

    # Processando DFC
    df_dfc = unificar_bases_dfc(RAW_DIR)
    df_dfc = transformar_dfc(df_dfc)
    valid_rows_dfc, errors_dfc = validar_dfc(df_dfc)

    if not errors_dfc:
        salvar_dfc(df_dfc)


    # Processando BP
    df_bp = unificar_bases_bp(RAW_DIR)
    df_bp = transformar_bp(df_bp)
    valid_rows_bp, errors_bp = validar_bp(df_bp)

    if not errors_bp:
        salvar_bp(df_bp)


    print("💾 Carregando no banco...")
    load_dre_to_db(df_dre)
    load_dfc_to_db(df_dfc)
    load_bp_to_db(df_bp)

    print("🧹 Limpando arquivos da pasta raw...")
    limpar_todos_csvs_raw()

   
    print("✅ Processamento concluído!")



if __name__ == "__main__":
    main()

