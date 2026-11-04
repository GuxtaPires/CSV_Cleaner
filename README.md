# 🧹 CSV Cleaner

Aplicação web desenvolvida em Python para análise, validação e tratamento de arquivos CSV. O projeto permite identificar problemas de qualidade nos dados, aplicar regras de limpeza e exportar arquivos tratados.

## 🚀 Funcionalidades

### 📊 Diagnóstico de dados
- Identificação da quantidade de linhas e colunas.
- Contagem de registros duplicados.
- Identificação de valores ausentes.
- Análise individual das colunas.
- Identificação de tipos de dados e valores únicos.
- Cálculo do percentual de valores ausentes por coluna.

### 🔎 Validação de dados
- Validação de colunas numéricas.
- Validação de datas.
- Identificação de valores incompatíveis com o tipo esperado.
- Exibição dos valores inconsistentes encontrados.

### 🧹 Limpeza e tratamento
- Remoção de linhas duplicadas.
- Remoção de espaços extras em textos.
- Padronização de textos vazios como valores ausentes.
- Conversão de colunas para formatos numéricos.
- Conversão de colunas para formatos de data.
- Substituição de valores inválidos por valores ausentes, sem excluir registros.

### 📥 Exportação
- Visualização dos dados originais e tratados.
- Download dos arquivos processados em CSV.

## 🛠️ Tecnologias utilizadas

- **Python:** linguagem principal.
- **Pandas:** manipulação, análise e tratamento de dados.
- **Streamlit:** desenvolvimento da interface web.

## 📁 Estrutura do projeto

```text
CSV_Cleaner/
├── app.py
├── cleaner.py
├── requirements.txt
├── README.md
└── data/
    └── dirty_cafe_sales.csv
```

## ⚙️ Como executar

**1. Clone o repositório**

```bash
git clone <URL_DO_REPOSITORIO>
cd CSV_Cleaner
```

**2. Crie o ambiente virtual**

```powershell
py -m venv .venv
```

**3. Ative o ambiente virtual**

```powershell
.\.venv\Scripts\Activate.ps1
```

**4. Instale as dependências**

```bash
py -m pip install -r requirements.txt
```

**5. Execute a aplicação**

```bash
py -m streamlit run app.py
```

A aplicação será aberta no navegador. Envie um arquivo CSV para iniciar o diagnóstico, validar os dados, aplicar tratamentos e exportar o resultado.

## 🎯 Objetivo do projeto

Desenvolver uma ferramenta prática de preparação e qualidade de dados, aplicando conceitos de manipulação de dados com Python, validação de informações e desenvolvimento de aplicações web.

O projeto também faz parte do meu desenvolvimento técnico nas áreas de **Data Analytics, Engenharia de Dados e Python**.

---

Desenvolvido como projeto de portfólio.
