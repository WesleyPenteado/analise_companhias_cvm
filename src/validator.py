from typing import List, Tuple
from schema import DRE_Schema


def validate_df_DRE(df) -> Tuple[List[DRE_Schema], List[dict]]:
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