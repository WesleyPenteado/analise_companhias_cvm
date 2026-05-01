# Download das Demonstrações Financeiras (Empresas CVM)

# Libraries
from pathlib import Path
import requests
import os
import io
import zipfile
import re

# 1. Criando Diretórios para os arquivos
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / 'data' / 'raw'
RAW_DIR.mkdir(parents=True, exist_ok=True) 


# 2. Acessando o material no endereço da CVM
dataset = 'cia_aberta-doc-dfp'
details_url = f"https://dados.cvm.gov.br/api/3/action/package_show?id={dataset}"
response = requests.get(details_url).json()

# 3. Verificando anos disponíveis

def get_available_years():
    '''Obtém os anos disponíveis para download dos arquivos zip da CVM.'''
    dataset = 'cia_aberta-doc-dfp'
    url = f"https://dados.cvm.gov.br/api/3/action/package_show?id={dataset}"

    response = requests.get(url)
    data = response.json()

    resources = data["result"]["resources"]

    anos = []

    for resource in resources:
        file_url = resource.get("url", "")
        
        match = re.search(r"dfp_cia_aberta_(\d{4})\.zip", file_url)
        if match:
            anos.append(int(match.group(1)))

    return sorted(set(anos))



# 3. Baixando e extraindo arquivos zip

def download_and_extract(ano: int, pasta_destino: str):
    '''Baixa e extrai o arquivo ZIP de todos os anos disponíveis para a pasta de destino data/raw.'''
    url = f"https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/dfp_cia_aberta_{ano}.zip"
    tipos = ["DRE", "DFC"] # BPA, BPP, DFC, DRE projeto final conterá estes arquivos

    
    print(f"Baixando arquivos do ano {ano}...")

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar {ano}: {e}")
        return

    try:
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            for file_name in zip_ref.namelist():
                if any(tipo in file_name for tipo in tipos):
                    zip_ref.extract(file_name, pasta_destino)
                    print(f"✅ Extraído: {file_name}")
    except zipfile.BadZipFile:
        print(f"❌ Arquivo ZIP inválido para o ano {ano}")

