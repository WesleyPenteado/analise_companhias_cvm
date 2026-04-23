# Criar PRD (Product Requirement Document) base do projeto

## *Problema*

    Usuários não têm acesso gratuito, estruturado e confiável para análise de demonstrações financeiras de empresas listadas na CVM.

## **Contexto e objetivo**

Atualmente diversas ferramentas propõem avaliar empresas listadas na bolsa de valores, porém nenhuma delas de forma visual, interativa e grátis.

Neste sentido o presente projeto objetiva a criação de uma aplicação onde será possível analisar a saúde financeira e possíveis tendências de forma profissional sobre estas empresas.

## Objetivo
Criar uma plataforma de dados financeiros que:

- Coleta dados públicos da CVM
- Garante qualidade via validação de schema
- Estrutura dados em modelo analítico
- Disponibiliza visualização interativa

## Arquitetura

[ Coleta ]  
   ↓  
[ Raw CSV ]  
   ↓  
[ Validação (Pydantic) ]  
   ↓  
[ Dados Limpos ]  
   ↓  
[ Data Warehouse (SQLAlchemy) ]  
   ↓  
[ Dashboard (Streamlit / Power BI) ]

## Estrutura

**Stack:**
- Python: 3.12.1
- Streamlit
- Pandas
- Pydantic
- sqlalchemy


project/  
│  
├── data/  
│   ├── raw/  
│   ├── clean/  
│  
├── src/  
│   ├── ingestion/  
│   ├── validation/  
│   ├── transformation/  
│   ├── database/  
│   ├── dashboard/  
│  
├── schemas/  
├── models/  
├── app/  
│   └── streamlit_app.py  
│  
├── main.py  


## Fora de escopo
- Machine Learning
- Previsão financeira
- Dados em tempo real

## Riscos e dependências
- CSVs inconsistentes da CVM
- Mudança no formato dos dados
