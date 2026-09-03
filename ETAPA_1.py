import pandas as pd
import json
import os
import glob
from google import genai
from google.genai import types
from openpyxl import load_workbook

# ==========================================
# 0. MAPEAMENTO DE PASTAS
# ==========================================
# O 'r' antes da string evita erros com as barras invertidas do Windows
pasta_checklist = r"C:\Users\joaomachado\Desktop\AUTOMATIZADOR_LEVANTAMENTOS\COLOQUE_AQUI_CHECKLIST"
pasta_base = r"C:\Users\joaomachado\Desktop\AUTOMATIZADOR_LEVANTAMENTOS\PLANILHA_BASE"

# O glob busca automaticamente arquivos com a extensão .xlsx nas pastas
try:
    # Pega o primeiro Excel que achar na pasta de checklist
    arquivo_checklist = glob.glob(os.path.join(pasta_checklist, "*.xlsx"))[0]
    
    # Pega o primeiro Excel que achar na pasta da planilha base genérica
    arquivo_destino = glob.glob(os.path.join(pasta_base, "*.xlsx"))[0]
    
    print(f"Checklist encontrado: {os.path.basename(arquivo_checklist)}")
    print(f"Planilha base encontrada: {os.path.basename(arquivo_destino)}")
    
except IndexError:
    print("Erro: Arquivo não encontrado! Certifique-se de que colocou os arquivos .xlsx nas pastas corretas.")
    exit() # Para a execução do script se não achar os arquivos

# ==========================================
# 1. EXTRAÇÃO E FILTRO DO CHECKLIST
# ==========================================
# Lendo a planilha pulando o cabeçalho
df_checklist = pd.read_excel(arquivo_checklist, sheet_name='Sheet1', skiprows=6)

# Renomeando colunas (Ajuste se o cabeçalho variar)
df_checklist.columns = ['Item', 'Qtd_Necessaria', 'Unidade', 'Qtd_Conferida', 'OK']

# Filtro: Pegar apenas onde a Quantidade Necessária é maior que 0
df_filtrado = df_checklist[pd.to_numeric(df_checklist['Qtd_Necessaria'], errors='coerce') > 0].copy()

# ==========================================
# 2. PREPARAÇÃO DO JSON PARA A IA
# ==========================================
lista_para_ia = []
for index, row in df_filtrado.iterrows():
    lista_para_ia.append({
        "nome": str(row['Item']),
        "quantidade": int(row['Qtd_Necessaria']),
        "tipo": "" # Espaço vazio para a IA preencher
    })

payload_json = json.dumps(lista_para_ia, ensure_ascii=False, indent=2)

# ==========================================
# 3. CHAMADA DA API DA IA
# ==========================================
CHAVE_API = "AQ.Ab8RN6Kc2dRCRuMph2GuBz2gTFshl6PGKp0OBbuQovDAMfmgzA" 

client = genai.Client(api_key=CHAVE_API)

prompt = f"""
Você é um classificador de materiais de infraestrutura. 
Analise a lista JSON abaixo. Para cada item, preencha a chave "tipo" com:
"E" se for um Equipamento.
"M" se for um Material de consumo/instalação.
Retorne APENAS o JSON preenchido.

Lista:
{payload_json}
"""

print("Consultando a IA para classificar os itens...")

resposta = client.models.generate_content(
    model='gemini-3.5-flash',
    contents=prompt,
    config={
        "response_mime_type": "application/json" # Força a saída ser um JSON limpo
    }
)

json_preenchido = json.loads(resposta.text.strip())
print("Classificação concluída!")

# ==========================================
# 4. SEPARAÇÃO NAS LISTAS 'E' E 'M'
# ==========================================
lista_m = [] 
lista_e = [] 

for item in json_preenchido:
    if item['tipo'] == 'M':
        lista_m.append(item)
    elif item['tipo'] == 'E':
        lista_e.append(item)

# ==========================================
# 5. INSERÇÃO NA PLANILHA GENÉRICA
# ==========================================
wb = load_workbook(arquivo_destino)
aba_materiais = wb['Materiais']
aba_equipamentos = wb['Equipamentos']

linha_inicio = 3

for i, mat in enumerate(lista_m):
    aba_materiais.cell(row=linha_inicio + i, column=2, value=mat['nome'])       
    aba_materiais.cell(row=linha_inicio + i, column=3, value=mat['quantidade']) 

for i, eqp in enumerate(lista_e):
    aba_equipamentos.cell(row=linha_inicio + i, column=2, value=eqp['nome'])       
    aba_equipamentos.cell(row=linha_inicio + i, column=3, value=eqp['quantidade']) 

# Criar o arquivo final na sua Área de Trabalho (ou outra pasta que preferir)
caminho_final = r"C:\Users\joaomachado\Desktop\AUTOMATIZADOR_LEVANTAMENTOS\LEVANTAMENTO_PREENCHIDO.xlsx"
wb.save(caminho_final)

print(f"Sucesso! A planilha foi preenchida e salva em:\n{caminho_final}")