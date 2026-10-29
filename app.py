import pandas as pd
import streamlit as st

# Importa as funções de limpeza criadas no cleaner.py.
from cleaner import (
    remover_duplicatas,
    limpar_espacos,
    padronizar_vazios,
)

# Configura a página da aplicação.
st.set_page_config(
    page_title="CSV Cleaner",
    page_icon="🧹",
    layout="wide"
)

# Exibe o título e uma breve descrição.
st.title("🧹 CSV Cleaner")
st.write("Analise, limpe e exporte seus arquivos CSV.")

# Cria um campo para o usuário enviar um arquivo CSV.
arquivo = st.file_uploader(
    "Envie seu arquivo CSV",
    type=["csv"]
)

# Só executa o processamento quando um arquivo é enviado.
if arquivo is not None:
    try:
        # Lê o CSV e transforma os dados em um DataFrame.
        df = pd.read_csv(arquivo)

        st.success("Arquivo carregado com sucesso!")

        # Exibe o diagnóstico dos dados originais.
        st.subheader("Diagnóstico original")

        # Divide a tela em quatro colunas para as métricas.
        col1, col2, col3, col4 = st.columns(4)

        # Quantidade de linhas e colunas do arquivo.
        col1.metric("Linhas", len(df))
        col2.metric("Colunas", len(df.columns))

        # Conta as linhas completamente duplicadas.
        col3.metric(
            "Duplicatas",
            int(df.duplicated().sum())
        )

        # Conta todas as células com valores ausentes.
        col4.metric(
            "Valores ausentes",
            int(df.isna().sum().sum())
        )

        # Cria uma seção expansível para visualizar os dados.
        with st.expander("Visualizar dados originais"):
            st.dataframe(
                df.head(100),
                use_container_width=True
            )

        st.divider()
        st.subheader("Configurar limpeza")

        # Cada checkbox permite ativar ou desativar uma regra.
        remover_dups = st.checkbox(
            "Remover linhas duplicadas",
            value=True
        )

        limpar_textos = st.checkbox(
            "Remover espaços extras dos textos",
            value=True
        )

        tratar_vazios = st.checkbox(
            "Padronizar textos vazios como valores ausentes",
            value=True
        )

        # Executa a limpeza somente quando o botão é clicado.
        if st.button("🧹 Limpar dados", type="primary"):

            # Cria uma cópia dos dados originais para trabalhar.
            df_limpo = df.copy()

            # Aplica a remoção de espaços, se selecionada.
            if limpar_textos:
                df_limpo = limpar_espacos(df_limpo)

            # Padroniza os textos vazios, se selecionado.
            if tratar_vazios:
                df_limpo = padronizar_vazios(df_limpo)

            # Remove as duplicatas, se selecionado.
            if remover_dups:
                df_limpo = remover_duplicatas(df_limpo)

            # Guarda os resultados na sessão do Streamlit.
            # Isso permite exibi-los mesmo após a atualização da tela.
            st.session_state["df_limpo"] = df_limpo
            st.session_state["df_original"] = df.copy()

        # Só exibe os resultados se uma limpeza já foi executada.
        if "df_limpo" in st.session_state:

            # Recupera os dados armazenados na sessão.
            df_limpo = st.session_state["df_limpo"]
            df_original = st.session_state["df_original"]

            st.divider()
            st.subheader("Resultado da limpeza")

            # Organiza as métricas dos dados tratados.
            col1, col2, col3 = st.columns(3)

            # Mostra a quantidade final de linhas e a variação.
            col1.metric(
                "Linhas finais",
                len(df_limpo),
                delta=len(df_limpo) - len(df_original)
            )

            # Mostra quantas duplicatas ainda existem.
            col2.metric(
                "Duplicatas restantes",
                int(df_limpo.duplicated().sum())
            )

            # Conta os valores ausentes após a limpeza.
            valores_ausentes = int(
                df_limpo.isna().sum().sum()
            )

            # Compara os valores ausentes com o arquivo original.
            ausentes_originais = int(
                df_original.isna().sum().sum()
            )

            col3.metric(
                "Valores ausentes",
                valores_ausentes,
                delta=valores_ausentes - ausentes_originais
            )

            # Exibe até 100 linhas do resultado.
            st.dataframe(
                df_limpo.head(100),
                use_container_width=True
            )

            # Converte o DataFrame para CSV e prepara os bytes
            # para que o navegador possa baixar o arquivo.
            csv_limpo = df_limpo.to_csv(
                index=False
            ).encode("utf-8-sig")

            # Cria o botão de download do arquivo tratado.
            st.download_button(
                label="⬇️ Baixar CSV limpo",
                data=csv_limpo,
                file_name="dados_limpos.csv",
                mime="text/csv"
            )

    # Exibe uma mensagem caso ocorra algum erro no processamento.
    except Exception as erro:
        st.error(f"Não foi possível processar o arquivo: {erro}")

# Mensagem exibida antes do envio de qualquer arquivo.
else:
    st.info("Envie um CSV para começar.")