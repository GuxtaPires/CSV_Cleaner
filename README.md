# 🧹 CSV Cleaner

Aplicação web desenvolvida em Python para facilitar a limpeza e a preparação de arquivos CSV, permitindo identificar problemas comuns, aplicar regras de tratamento e exportar os dados limpos.

## 🚀 Funcionalidades

- Upload de arquivos CSV.
- Diagnóstico inicial com quantidade de linhas, colunas, duplicatas e valores ausentes.
- Visualização dos dados originais.
- Remoção de linhas duplicadas.
- Remoção de espaços extras em textos.
- Padronização de textos vazios como valores ausentes.
- Visualização dos resultados após a limpeza.
- Download do arquivo CSV tratado.

## 🛠️ Tecnologias

- Python
- Pandas
- Streamlit

## ⚙️ Como executar

**1. Clone o repositório**

```bash
git clone <URL_DO_REPOSITORIO>
cd CSV_Cleaner
```

**2. Crie e ative o ambiente virtual**

No Windows:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**3. Instale as dependências**

```bash
py -m pip install -r requirements.txt
```

**4. Execute a aplicação**

```bash
py -m streamlit run app.py
```

A aplicação será aberta no navegador. Envie um arquivo CSV, selecione as regras desejadas, execute a limpeza e baixe o resultado.

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

## 🎯 Objetivo

Projeto de portfólio voltado à prática de Python, manipulação de dados com Pandas e desenvolvimento de aplicações para automatizar tarefas de preparação de dados.

---

Desenvolvido como projeto de aprendizado em **Python e Data Analytics**.