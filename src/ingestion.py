# Download das Demonstrações Financeiras (Empresas CVM)

# Libraries
import sys
import pandas as pd
import requests
import os
import io
import zipfile
import numpy as np


# 1. Acessando o material no endereço da CVM
dataset = 'cia_aberta-doc-dfp'
details_url = f"https://dados.cvm.gov.br/api/3/action/package_show?id={dataset}"
response = requests.get(details_url).json()

# 2. Baixando arquivos zip

anos = [2020, 2021, 2022, 2023, 2024, 2025]

for ano in anos:
    url = f"https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/dfp_cia_aberta_{ano}.zip"
    destino = f"dfp_{ano}.zip"
    pasta_destino = "data/raw"
    os.makedirs(pasta_destino, exist_ok=True) # Criar pasta se não existir
    
    print(f" Baixando arquivos do ano {ano}...")
    response = requests.get(url)
    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(pasta_destino)
            print(" Arquivos baixados e extraídos com sucesso!")
    else:
        print(f" Falha ao baixar arquivos do ano {ano}. Status code: {response.status_code}")

