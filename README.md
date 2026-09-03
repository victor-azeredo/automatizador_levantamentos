# ⚙️ Automatizador de Custos Operacionais

## 📖 Sobre o Projeto
Software em Python desenvolvido para automatizar e otimizar o processo de levantamento de custos logísticos e operacionais. O sistema atua como um pipeline de dados (ETL) que cruza informações de checklists técnicos com arquivos PDF de Ordens de Compra (POs) e Notas Fiscais. 

O objetivo principal é eliminar o trabalho braçal de conferência de itens, utilizando Inteligência Artificial para classificação e algoritmos de *Fuzzy Matching* para encontrar correspondências de preços, unificando todo o balanço financeiro em uma única planilha finalizada.

## 🚀 Funcionalidades
- **Leitura e Filtragem:** Extração de itens a partir de planilhas genéricas de checklist.
- **Classificação via IA:** Integração com a API do Google Gemini para categorizar o payload de itens automaticamente entre Equipamentos (E) ou Materiais (M).
- **Extração de Dados em PDFs:** Varredura em lote para leitura de POs e extração de descrições e valores unitários utilizando Regex.
- **Cruzamento Inteligente (Fuzzy Matching):** Comparação de similaridade de strings para cruzar com precisão os itens do checklist com os itens faturados, ignorando diferenças de digitação (ex: maiúsculas/minúsculas e ordem das palavras).
- **Exportação Preservada:** Inserção dos dados processados na planilha final de levantamento de custos mantendo as cores, layout e formatação original intactos.

## 🛠️ Tecnologias Utilizadas
* **[Python 3.8+](https://www.python.org/)** - Linguagem principal do projeto.
* **[Pandas](https://pandas.pydata.org/)** - Estruturação e manipulação inicial dos dados.
* **[Openpyxl](https://openpyxl.readthedocs.io/)** - Escrita cirúrgica na planilha Excel final.
* **[pdfplumber](https://github.com/jsvine/pdfplumber)** - Leitura e extração estruturada de textos em arquivos PDF.
* **[TheFuzz](https://github.com/seatgeek/thefuzz)** - Algoritmo de distância de Levenshtein para similaridade de textos.
* **[Google Generative AI](https://aistudio.google.com/)** - Uso da API Gemini para classificação semântica de materiais.

## ⚙️ Pré-requisitos
Antes de começar, você precisará ter instalado em sua máquina:
* [Python](https://www.python.org/downloads/)
* Uma chave de API gratuita do [Google AI Studio](https://aistudio.google.com/)

## 📦 Instalação

**1. Clone o repositório:**
```bash
git clone [https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git](https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git)
cd NOME_DO_REPOSITORIO
```

**2. Instale as dependências necessárias:**
Recomenda-se o uso de um ambiente virtual (venv). Execute o comando abaixo para instalar todas as bibliotecas:
```bash
pip install pandas openpyxl pdfplumber thefuzz google-genai
```

## 🔑 Configuração
Abra o arquivo .env_exemplo do script e insira a sua chave de API na variável correspondente:
```python
API_KEY = COLOQUE_SUA_CHAVE_GERADA_AQUI
```
## 🚀 Como Executar
Com a chave configurada e os arquivos base posicionados nas pastas do projeto, basta rodar o script no seu terminal:
```bash
python ETAPA_1.py
```
O sistema irá ler os PDFs, cruzar os dados, acionar a inteligência artificial e gerar o arquivo `LEVANTAMENTO_PREENCHIDO.xlsx` contendo todo o consolidado de custos.
