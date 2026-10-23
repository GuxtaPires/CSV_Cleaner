import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="CSV Cleaner",
    page_icon="🧹",
    layout="wide"
)

st.title("🧹 CSV Cleaner")
st.write("Envie um CSV para analisar e limpar seus dados.")

arquivo = st.file_uploader(
    "Selecione seu arquivo CSV",
    type=["csv"]
)

if arquivo is not None:
    try:
        df = pd.read_csv(arquivo)

        st.success("Arquivo carregado com sucesso!")

        col1, col2 = st.columns(2)

        col1.metric("Linhas", len(df))
        col2.metric("Colunas", len(df.columns))

        st.subheader("Prévia dos dados")
        st.dataframe(df.head(20), use_container_width=True)

    except Exception as erro:
        st.error(f"Não foi possível ler o arquivo: {erro}")
