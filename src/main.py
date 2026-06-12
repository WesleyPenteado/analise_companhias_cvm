from src.ingestion import get_available_years, download_and_extract
from src.transformation_dre import unificar_bases_dre, transformar_dre, validar_dre, salvar_dre, limpar_todos_csvs_raw
from src.load import load_dre_to_db
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
    df = unificar_bases_dre(RAW_DIR)
    df = transformar_dre(df)
    valid_rows, errors = validar_dre(df)

    if not errors:
        salvar_dre(df)
    
    print("💾 Carregando no banco...")
    load_dre_to_db(df)

    print("🧹 Limpando arquivos da pasta raw...")
    limpar_todos_csvs_raw()

   
    print("✅ Processamento concluído!")



if __name__ == "__main__":
    main()

