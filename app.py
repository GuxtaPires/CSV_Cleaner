import pandas as pd
import streamlit as st

# Importa as funções de limpeza e diagnóstico.
from cleaner import (
    remover_duplicatas,
    limpar_espacos,
    padronizar_vazios,
    diagnostico_colunas,
    validar_coluna
)


# ==========================================
# CONFIGURAÇÕES DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="CSV Cleaner",
    page_icon="🧹",
    layout="wide"
)

st.title("🧹 CSV Cleaner")
st.write("Analise, valide, limpe e exporte seus arquivos CSV.")


# ==========================================
# UPLOAD DO ARQUIVO
# ==========================================

arquivo = st.file_uploader(
    "Envie seu arquivo CSV",
    type=["csv"]
)


if arquivo is not None:

    try:

        # Lê o arquivo e transforma em DataFrame.
        df = pd.read_csv(arquivo)

        # Identifica quando um novo arquivo é enviado.
        identificador_arquivo = (
            arquivo.name,
            arquivo.size
        )

        # Limpa resultados antigos quando o arquivo muda.
        if st.session_state.get("arquivo_atual") != identificador_arquivo:

            st.session_state["arquivo_atual"] = identificador_arquivo

            for chave in [
                "df_limpo",
                "df_original",
                "resultado_validacao"
            ]:
                st.session_state.pop(chave, None)

        st.success("Arquivo carregado com sucesso!")


        # ==========================================
        # DIAGNÓSTICO GERAL
        # ==========================================

        st.subheader("Diagnóstico original")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Linhas", len(df))

        col2.metric("Colunas", len(df.columns))

        col3.metric(
            "Duplicatas",
            int(df.duplicated().sum())
        )

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

            diagnostico = diagnostico_colunas(df)

            st.dataframe(
                diagnostico,
                use_container_width=True,
                hide_index=True
            )


        st.divider()


        # ==========================================
        # VALIDAÇÃO DE TIPOS DE DADOS
        # ==========================================

        st.subheader("Validação de dados")

        st.write(
            "Selecione uma coluna e informe qual tipo de dado "
            "você espera encontrar nela."
        )

        # Permite selecionar uma coluna do arquivo.
        coluna_selecionada = st.selectbox(
            "Selecione a coluna",
            options=list(df.columns)
        )

        # Permite escolher o tipo esperado.
        tipo_esperado = st.selectbox(
            "Tipo de dado esperado",
            options=["Numérico", "Data"]
        )

        # Executa a validação quando o botão é clicado.
        if st.button("🔎 Validar coluna"):

            resultado = validar_coluna(
                df,
                coluna_selecionada,
                tipo_esperado
            )

            # Guarda o resultado na sessão.
            st.session_state["resultado_validacao"] = {
                "coluna": coluna_selecionada,
                "tipo": tipo_esperado,
                "resultado": resultado
            }

        # Exibe o resultado da última validação.
        if "resultado_validacao" in st.session_state:

            dados = st.session_state["resultado_validacao"]

            resultado = dados["resultado"]

            # Garante que o resultado exibido pertence
            # à coluna e ao tipo atualmente selecionados.
            if (
                dados["coluna"] == coluna_selecionada
                and dados["tipo"] == tipo_esperado
            ):

                st.markdown("### Resultado da validação")

                # Organiza as métricas em quatro colunas.
                col1, col2, col3, col4 = st.columns(4)

                col1.metric(
                    "Valores analisados",
                    resultado["total"]
                )

                col2.metric(
                    "Valores válidos",
                    resultado["validos"]
                )

                col3.metric(
                    "Valores inválidos",
                    resultado["invalidos"]
                )

                col4.metric(
                    "% Inválidos",
                    f'{resultado["percentual_invalidos"]}%'
                )

                # Exibe os valores problemáticos.
                if resultado["invalidos"] > 0:

                    st.warning(
                        "Foram encontrados valores inconsistentes."
                    )

                    st.dataframe(
                        resultado["detalhes"],
                        use_container_width=True,
                        hide_index=True
                    )

                else:

                    st.success(
                        "Nenhuma inconsistência encontrada "
                        "para o tipo selecionado!"
                    )


        st.divider()


        # ==========================================
        # CONFIGURAÇÃO DA LIMPEZA
        # ==========================================

        st.subheader("Configurar limpeza")

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

            # Aplica as regras selecionadas.
            if limpar_textos:
                df_limpo = limpar_espacos(df_limpo)

            if tratar_vazios:
                df_limpo = padronizar_vazios(df_limpo)

            if remover_dups:
                df_limpo = remover_duplicatas(df_limpo)

            # Armazena os resultados na sessão.
            st.session_state["df_limpo"] = df_limpo
            st.session_state["df_original"] = df.copy()


        # ==========================================
        # RESULTADO DA LIMPEZA
        # ==========================================

        if "df_limpo" in st.session_state:

            df_limpo = st.session_state["df_limpo"]

            df_original = st.session_state["df_original"]

            st.divider()

            st.subheader("Resultado da limpeza")

            col1, col2, col3 = st.columns(3)

            # Quantidade final de linhas.
            col1.metric(
                "Linhas finais",
                len(df_limpo),
                delta=len(df_limpo) - len(df_original)
            )

            # Duplicatas restantes.
            col2.metric(
                "Duplicatas restantes",
                int(df_limpo.duplicated().sum())
            )

            # Valores ausentes antes e depois.
            ausentes_originais = int(
                df_original.isna().sum().sum()
            )

            ausentes_finais = int(
                df_limpo.isna().sum().sum()
            )

            col3.metric(
                "Valores ausentes",
                ausentes_finais,
                delta=ausentes_finais - ausentes_originais
            )

            # Visualização dos dados tratados.
            st.dataframe(
                df_limpo.head(100),
                use_container_width=True
            )


            # ==========================================
            # DOWNLOAD DO CSV LIMPO
            # ==========================================

            # Converte o DataFrame para CSV.
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


    # ==========================================
    # TRATAMENTO DE ERROS
    # ==========================================

    except Exception as erro:

        st.error(
            f"Não foi possível processar o arquivo: {erro}"
        )


# Mensagem exibida antes do upload.
else:

    st.info("Envie um CSV para começar.")