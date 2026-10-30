import pandas as pd
import streamlit as st

# Importa as funções de limpeza e diagnóstico.
from cleaner import (
    remover_duplicatas,
    limpar_espacos,
    padronizar_vazios,
    diagnostico_colunas,
)


# ==========================================
# CONFIGURAÇÕES DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="CSV Cleaner",
    page_icon="🧹",
    layout="wide"
)

# Título e descrição da aplicação.
st.title("🧹 CSV Cleaner")
st.write("Analise, limpe e exporte seus arquivos CSV.")


# ==========================================
# UPLOAD DO ARQUIVO
# ==========================================

# Permite ao usuário enviar um arquivo CSV.
arquivo = st.file_uploader(
    "Envie seu arquivo CSV",
    type=["csv"]
)


# Executa o restante da aplicação somente
# quando um arquivo é enviado.
if arquivo is not None:

    try:
        # Lê o arquivo e transforma em DataFrame.
        df = pd.read_csv(arquivo)

        st.success("Arquivo carregado com sucesso!")

        # ==========================================
        # DIAGNÓSTICO GERAL
        # ==========================================

        st.subheader("Diagnóstico original")

        # Divide a área em quatro colunas.
        col1, col2, col3, col4 = st.columns(4)

        # Exibe a quantidade de linhas.
        col1.metric("Linhas", len(df))

        # Exibe a quantidade de colunas.
        col2.metric("Colunas", len(df.columns))

        # Conta as linhas duplicadas.
        col3.metric(
            "Duplicatas",
            int(df.duplicated().sum())
        )

        # Conta todos os valores ausentes.
        col4.metric(
            "Valores ausentes",
            int(df.isna().sum().sum())
        )

        # ==========================================
        # VISUALIZAÇÃO DOS DADOS ORIGINAIS
        # ==========================================

        with st.expander("Visualizar dados originais"):

            st.dataframe(
                df.head(100),
                use_container_width=True
            )

        # ==========================================
        # DIAGNÓSTICO POR COLUNA
        # ==========================================

        with st.expander("Diagnóstico por coluna"):

            # Executa o diagnóstico detalhado.
            diagnostico = diagnostico_colunas(df)

            # Exibe os resultados em formato de tabela.
            st.dataframe(
                diagnostico,
                use_container_width=True,
                hide_index=True
            )

        st.divider()

        # ==========================================
        # CONFIGURAÇÃO DA LIMPEZA
        # ==========================================

        st.subheader("Configurar limpeza")

        # Permite escolher quais regras serão aplicadas.
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

        # ==========================================
        # EXECUÇÃO DA LIMPEZA
        # ==========================================

        if st.button("🧹 Limpar dados", type="primary"):

            # Cria uma cópia dos dados originais.
            df_limpo = df.copy()

            # Aplica cada regra conforme a seleção.
            if limpar_textos:
                df_limpo = limpar_espacos(df_limpo)

            if tratar_vazios:
                df_limpo = padronizar_vazios(df_limpo)

            if remover_dups:
                df_limpo = remover_duplicatas(df_limpo)

            # Guarda os resultados na sessão do Streamlit.
            st.session_state["df_limpo"] = df_limpo
            st.session_state["df_original"] = df.copy()

        # ==========================================
        # RESULTADO DA LIMPEZA
        # ==========================================

        # Verifica se uma limpeza já foi executada.
        if "df_limpo" in st.session_state:

            # Recupera os DataFrames armazenados.
            df_limpo = st.session_state["df_limpo"]
            df_original = st.session_state["df_original"]

            st.divider()
            st.subheader("Resultado da limpeza")

            # Organiza as métricas em três colunas.
            col1, col2, col3 = st.columns(3)

            # Mostra a quantidade final de linhas.
            # O delta indica a diferença em relação ao original.
            col1.metric(
                "Linhas finais",
                len(df_limpo),
                delta=len(df_limpo) - len(df_original)
            )

            # Mostra quantas duplicatas restaram.
            col2.metric(
                "Duplicatas restantes",
                int(df_limpo.duplicated().sum())
            )

            # Calcula os valores ausentes antes e depois.
            ausentes_originais = int(
                df_original.isna().sum().sum()
            )

            ausentes_finais = int(
                df_limpo.isna().sum().sum()
            )

            # Exibe a quantidade de valores ausentes.
            col3.metric(
                "Valores ausentes",
                ausentes_finais,
                delta=ausentes_finais - ausentes_originais
            )

            # Exibe uma prévia dos dados tratados.
            st.dataframe(
                df_limpo.head(100),
                use_container_width=True
            )

            # ==========================================
            # DOWNLOAD DO CSV LIMPO
            # ==========================================

            # Converte o DataFrame para CSV.
            # utf-8-sig ajuda na compatibilidade com Excel.
            csv_limpo = df_limpo.to_csv(
                index=False
            ).encode("utf-8-sig")

            # Disponibiliza o arquivo para download.
            st.download_button(
                label="⬇️ Baixar CSV limpo",
                data=csv_limpo,
                file_name="dados_limpos.csv",
                mime="text/csv"
            )

    # Trata erros durante a leitura ou processamento.
    except Exception as erro:

        st.error(
            f"Não foi possível processar o arquivo: {erro}"
        )


# Mensagem inicial, antes do envio de um arquivo.
else:

    st.info("Envie um CSV para começar.")