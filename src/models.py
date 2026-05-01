from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

Base = declarative_base()

class DRE(Base):
    __tablename__ = "dre_con"
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