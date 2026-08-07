from sqlalchemy import Column, Integer, String, Date, Numeric, Index
from sqlalchemy.orm import declarative_base
from src.database import cvm_base, view_base


class DRE_Model(cvm_base):
    __tablename__ = "dre"

    id = Column(Integer, primary_key=True, autoincrement=True)

    CNPJ_CIA = Column(String, nullable=False)
    DT_REFER = Column(Date, nullable=True)
    VERSAO = Column(Integer, nullable=False)
    DENOM_CIA = Column(String, nullable=False)
    CD_CVM = Column(Integer, nullable=False)
    GRUPO_DFP = Column(String, nullable=False)
    MOEDA = Column(String, nullable=False)
    ESCALA_MOEDA = Column(String, nullable=True)
    ORDEM_EXERC = Column(String, nullable=True)
    DT_INI_EXERC = Column(Date, nullable=True)
    DT_FIM_EXERC = Column(Date, nullable=True)
    CD_CONTA = Column(String, nullable=False)
    DS_CONTA = Column(String, nullable=False)
    VL_CONTA = Column(Numeric(20, 4), nullable=False)
    ST_CONTA_FIXA = Column(String(1), nullable=False)  # "S" ou "N"
    ANO = Column(Integer, nullable=True)

class DFC_Model(cvm_base):
    __tablename__ = "dfc"

    id = Column(Integer, primary_key=True, autoincrement=True)

    CNPJ_CIA = Column(String, nullable=False)
    DT_REFER = Column(Date, nullable=True)
    VERSAO = Column(Integer, nullable=False)
    DENOM_CIA = Column(String, nullable=False)
    CD_CVM = Column(Integer, nullable=False)
    GRUPO_DFP = Column(String, nullable=False)
    MOEDA = Column(String, nullable=False)
    ESCALA_MOEDA = Column(String, nullable=True)
    ORDEM_EXERC = Column(String, nullable=True)
    DT_INI_EXERC = Column(Date, nullable=True)
    DT_FIM_EXERC = Column(Date, nullable=True)
    CD_CONTA = Column(String, nullable=False)
    DS_CONTA = Column(String, nullable=False)
    VL_CONTA = Column(Numeric(20, 4), nullable=False)
    ST_CONTA_FIXA = Column(String(1), nullable=False)  # "S" ou "N"
    ANO = Column(Integer, nullable=True)

class BP_Model(cvm_base):
    __tablename__ = "bp"

    id = Column(Integer, primary_key=True, autoincrement=True)

    CNPJ_CIA = Column(String, nullable=False)
    DT_REFER = Column(Date, nullable=True)
    VERSAO = Column(Integer, nullable=False)
    DENOM_CIA = Column(String, nullable=False)
    CD_CVM = Column(Integer, nullable=False)
    GRUPO_DFP = Column(String, nullable=False)
    MOEDA = Column(String, nullable=False)
    ESCALA_MOEDA = Column(String, nullable=True)
    ORDEM_EXERC = Column(String, nullable=True)
    DT_FIM_EXERC = Column(Date, nullable=True)
    CD_CONTA = Column(String, nullable=False)
    DS_CONTA = Column(String, nullable=False)
    VL_CONTA = Column(Numeric(20, 4), nullable=False)
    ST_CONTA_FIXA = Column(String(1), nullable=False)  # "S" ou "N"
    ANO = Column(Integer, nullable=True)

    __table_args__ = (
            Index("idx_bp_lookup", "DENOM_CIA", "GRUPO_DFP", "CD_CONTA", "ANO"),
        )

class View_BP_Tipo_Anual_Model(view_base):
    __tablename__ = "vw_bp_tipo_anual"

    DENOM_CIA = Column(String, primary_key=True)
    GRUPO_DFP = Column(String, primary_key=True)
    ANO = Column(Integer, primary_key=True)

    tipo_empresa = Column(String)


class View_BP_Tipo_Empresa_Model(view_base):
    __tablename__ = "vw_bp_tipo_empresa"

    DENOM_CIA = Column(String, primary_key=True)
    GRUPO_DFP = Column(String, primary_key=True)
    ANO = Column(Integer, primary_key=True)

    tipo_empresa = Column(String)
    tipo_atual = Column(String)
    considerar = Column(Integer)