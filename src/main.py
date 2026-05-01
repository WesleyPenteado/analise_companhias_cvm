from transformation import unificar_bases_dre_con
from load import load_dre_to_db, load_to_db

RAW_DIR = "data/raw"

def run_pipeline():
    df = unificar_bases_dre_con(RAW_DIR)
    load_dre_to_db(df)

if __name__ == "__main__":
    run_pipeline()