from typing import List, Tuple
from src.schema import DRE_Schema


def validador_df_DRE(df) -> Tuple[List[DRE_Schema], List[dict]]:
    '''Valida o DataFrame de DRE usando o Pydantic. Retorna uma lista de linhas válidas e uma lista de erros encontrados.'''
    valid_rows = []
    errors = []

    for i, row in df.iterrows():
        try:
            valid = DRE_Schema(**row.to_dict())
            valid_rows.append(valid)

        except Exception as e:
            errors.append({
                "index": i,
                "error": str(e),
                "row": row.to_dict()
            })

    return valid_rows, errors