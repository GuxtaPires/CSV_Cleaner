
import pandas as pd
import streamlit as st

from cleaner import (
    remover_duplicatas,
    limpar_espacos,
    padronizar_vazios,
)

# Configuração da página
st.set_page_config(
    page_title="CSV Cleaner",
    page_icon="🧹",
    layout="wide",
)

st.title("🧹 CSV Cleaner")
st.write("Analise, limpe e exporte seus arquivos CSV.")

# Upload
arquivo = st.file_uploader(
    "Envie seu arquivo CSV",
    type=["csv"],
)

if arquivo is not None:
    try:
        df = pd.read_csv(arquivo)

        st.success("Arquivo carregado com sucesso!")

        st.subheader("Diagnóstico original")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Linhas", len(df))
        col2.metric("Colunas", len(df.columns))
        col3.metric("Duplicatas", int(df.duplicated().sum()))
        col4.metric("Valores ausentes", int(df.isna().sum().sum()))

        with st.expander("Visualizar dados originais"):
            st.dataframe(df.head(100), use_container_width=True)

        st.divider()
        st.subheader("Configurar limpeza")

        remover_dups = st.checkbox(
            "Remover linhas duplicadas",
            value=True,
        )

        limpar_textos = st.checkbox(
            "Remover espaços extras dos textos",
            value=True,
        )

        tratar_vazios = st.checkbox(
            "Padronizar textos vazios como valores ausentes",
            value=True,
        )

        if st.button("🧹 Limpar dados", type="primary"):
            df_limpo = df.copy()

            if limpar_textos:
                df_limpo = limpar_espacos(df_limpo)

            if tratar_vazios:
                df_limpo = padronizar_vazios(df_limpo)

            if remover_dups:
                df_limpo = remover_duplicatas(df_limpo)

            st.session_state["df_limpo"] = df_limpo
            st.session_state["df_original"] = df.copy()

        if "df_limpo" in st.session_state:
            df_limpo = st.session_state["df_limpo"]
            df_original = st.session_state["df_original"]

            st.divider()
            st.subheader("Resultado da limpeza")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Linhas finais",
                len(df_limpo),
                delta=len(df_limpo) - len(df_original),
            )

            col2.metric(
                "Duplicatas restantes",
                int(df_limpo.duplicated().sum()),
            )

            col3.metric(
                "Valores ausentes",
                int(df_limpo.isna().sum().sum()),
                delta=(
                    int(df_limpo.isna().sum().sum())
                    - int(df_original.isna().sum().sum())
                ),
            )

            st.dataframe(
                df_limpo.head(100),
                use_container_width=True,
            )

            csv_limpo = df_limpo.to_csv(
                index=False,
            ).encode("utf-8-sig")

            st.download_button(
                label="⬇️ Baixar CSV limpo",
                data=csv_limpo,
                file_name="dados_limpos.csv",
                mime="text/csv",
            )

    except Exception as erro:
        st.error(f"Não foi possível processar o arquivo: {erro}")

else:
    st.info("Envie um CSV para começar.")
