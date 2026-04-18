from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import date
from decimal import Decimal


class DRE_Schema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    CNPJ_CIA: str
    DT_REFER: date
    VERSAO: int
    DENOM_CIA: str
    CD_CVM: int
    GRUPO_DFP: str
    MOEDA: str
    ESCALA_MOEDA: Literal["UNIDADE", "MIL", "MILHAR", "MILHÃO"]
    ORDEM_EXERC: Literal["ÚLTIMO", "PENÚLTIMO"]
    DT_INI_EXERC: date
    DT_FIM_EXERC: date
    CD_CONTA: str
    DS_CONTA: str
    VL_CONTA: Decimal
    ST_CONTA_FIXA: Literal["S", "N"]