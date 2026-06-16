from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import date
from decimal import Decimal


class DRE_Schema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    CNPJ_CIA: str
    DT_REFER: Optional[date]
    VERSAO: int
    DENOM_CIA: str
    CD_CVM: int
    GRUPO_DFP: str
    MOEDA: str
    ESCALA_MOEDA: Optional[str]
    ORDEM_EXERC: Optional[str]
    DT_INI_EXERC: Optional[date]
    DT_FIM_EXERC: Optional[date]
    CD_CONTA: str
    DS_CONTA: str
    VL_CONTA: Decimal
    ST_CONTA_FIXA: Literal["S", "N"]
    ANO: Optional[int]

class DFC_Schema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    CNPJ_CIA: str
    DT_REFER: Optional[date]
    VERSAO: int
    DENOM_CIA: str
    CD_CVM: int
    GRUPO_DFP: str
    MOEDA: str
    ESCALA_MOEDA: Optional[str]
    ORDEM_EXERC: Optional[str]
    DT_INI_EXERC: Optional[date]
    DT_FIM_EXERC: Optional[date]
    CD_CONTA: str
    DS_CONTA: str
    VL_CONTA: Decimal
    ST_CONTA_FIXA: Literal["S", "N"]
    ANO: Optional[int]



