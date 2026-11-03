import pandas as pd
import streamlit as st

# Importa as funções de limpeza, validação e tratamento.
from cleaner import (
    remover_duplicatas,
    limpar_espacos,
    padronizar_vazios,
    diagnostico_colunas,
    validar_coluna,
    tratar_coluna
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
        # Lê o CSV e transforma os dados em DataFrame.
        df = pd.read_csv(arquivo)

        # Identifica o arquivo enviado.
        identificador_arquivo = (
            arquivo.name,
            arquivo.size
        )

        # Limpa resultados anteriores quando o arquivo muda.
        if st.session_state.get("arquivo_atual") != identificador_arquivo:

            st.session_state["arquivo_atual"] = identificador_arquivo

            for chave in [
                "df_limpo",
                "df_original",
                "df_tratado",
                "resultado_validacao",
                "coluna_tratada",
                "tipo_tratamento"
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
        # VALIDAÇÃO DE DADOS
        # ==========================================

        st.subheader("Validação de dados")

        st.write(
            "Selecione uma coluna e informe qual tipo "
            "de dado você espera encontrar nela."
        )

        coluna_validacao = st.selectbox(
            "Coluna para validação",
            options=list(df.columns),
            key="coluna_validacao"
        )

        tipo_validacao = st.selectbox(
            "Tipo esperado",
            options=["Numérico", "Data"],
            key="tipo_validacao"
        )

        if st.button("🔎 Validar coluna"):

            resultado = validar_coluna(
                df,
                coluna_validacao,
                tipo_validacao
            )

            st.session_state["resultado_validacao"] = {
                "coluna": coluna_validacao,
                "tipo": tipo_validacao,
                "resultado": resultado
            }

        # Recupera e apresenta a última validação.
        if "resultado_validacao" in st.session_state:

            dados_validacao = st.session_state[
                "resultado_validacao"
            ]

            if (
                dados_validacao["coluna"] == coluna_validacao
                and dados_validacao["tipo"] == tipo_validacao
            ):

                resultado = dados_validacao["resultado"]

                st.markdown("### Resultado da validação")

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
                        "Nenhuma inconsistência encontrada!"
                    )


        st.divider()


        # ==========================================
        # TRATAMENTO DE INCONSISTÊNCIAS
        # ==========================================

        st.subheader("Tratamento de inconsistências")

        st.write(
            "Escolha uma coluna e o tipo esperado para "
            "converter os valores. Os valores inválidos "
            "serão transformados em valores ausentes."
        )

        coluna_tratamento = st.selectbox(
            "Coluna para tratamento",
            options=list(df.columns),
            key="coluna_tratamento"
        )

        tipo_tratamento = st.selectbox(
            "Tipo de conversão",
            options=["Numérico", "Data"],
            key="tipo_tratamento"
        )

        # Explica o que acontecerá com os dados.
        st.info(
            "O tratamento não exclui linhas. "
            "Valores que não puderem ser convertidos "
            "serão transformados em valores ausentes."
        )

        if st.button("⚙️ Aplicar tratamento"):

            # Usa os dados já limpos, caso a limpeza básica
            # tenha sido executada. Caso contrário, usa o original.
            df_base = st.session_state.get("df_limpo", df)

            # Aplica o tratamento na coluna selecionada.
            df_tratado = tratar_coluna(
                df_base,
                coluna_tratamento,
                tipo_tratamento
            )

            # Armazena o resultado na sessão.
            st.session_state["df_tratado"] = df_tratado

            st.session_state["coluna_tratada"] = coluna_tratamento

            st.session_state["tipo_tratamento"] = tipo_tratamento

        # Exibe o resultado do tratamento.
        if "df_tratado" in st.session_state:

            df_tratado = st.session_state["df_tratado"]

            coluna_salva = st.session_state["coluna_tratada"]

            tipo_salvo = st.session_state["tipo_tratamento"]

            # Evita mostrar um resultado antigo como se fosse novo.
            if (
                coluna_salva == coluna_tratamento
                and tipo_salvo == tipo_tratamento
            ):

                st.markdown("### Resultado do tratamento")

                # Compara a quantidade de valores ausentes
                # antes e depois da conversão.
                df_base = st.session_state.get("df_limpo", df)

                ausentes_antes = int(
                    df_base[coluna_tratada].isna().sum()
                )

                ausentes_depois = int(
                    df_tratado[coluna_tratada].isna().sum()
                )

                novos_ausentes = ausentes_depois - ausentes_antes

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Linhas preservadas",
                    len(df_tratado)
                )

                col2.metric(
                    "Novos valores ausentes",
                    novos_ausentes
                )

                col3.metric(
                    "Tipo resultante",
                    str(df_tratado[coluna_tratada].dtype)
                )

                st.dataframe(
                    df_tratado.head(100),
                    use_container_width=True
                )


        st.divider()


        # ==========================================
        # LIMPEZA BÁSICA
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

        if st.button("🧹 Limpar dados", type="primary"):

            # Começa com uma cópia dos dados originais.
            df_limpo = df.copy()

            # Aplica as regras selecionadas.
            if limpar_textos:
                df_limpo = limpar_espacos(df_limpo)

            if tratar_vazios:
                df_limpo = padronizar_vazios(df_limpo)

            if remover_dups:
                df_limpo = remover_duplicatas(df_limpo)

            # Armazena o resultado da limpeza.
            st.session_state["df_limpo"] = df_limpo
            st.session_state["df_original"] = df.copy()

            # Descarta tratamentos anteriores,
            # pois a base utilizada foi atualizada.
            st.session_state.pop("df_tratado", None)
            st.session_state.pop("coluna_tratada", None)
            st.session_state.pop("tipo_tratamento", None)


        # ==========================================
        # RESULTADO DA LIMPEZA
        # ==========================================

        if "df_limpo" in st.session_state:

            df_limpo = st.session_state["df_limpo"]

            df_original = st.session_state["df_original"]

            st.divider()
            st.subheader("Resultado da limpeza")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Linhas finais",
                len(df_limpo),
                delta=len(df_limpo) - len(df_original)
            )

            col2.metric(
                "Duplicatas restantes",
                int(df_limpo.duplicated().sum())
            )

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

            st.dataframe(
                df_limpo.head(100),
                use_container_width=True
            )


        # ==========================================
        # DOWNLOAD DOS DADOS
        # ==========================================

        # Prioriza o resultado do tratamento, se existir.
        # Caso contrário, disponibiliza os dados limpos
        # ou, na ausência de limpeza, os dados originais.

        if "df_tratado" in st.session_state:

            df_exportar = st.session_state["df_tratado"]

        elif "df_limpo" in st.session_state:

            df_exportar = st.session_state["df_limpo"]

        else:

            df_exportar = df

        # Converte os dados para CSV.
        csv_final = df_exportar.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            label="⬇️ Baixar CSV final",
            data=csv_final,
            file_name="dados_tratados.csv",
            mime="text/csv"
        )


    except Exception as erro:

        st.error(
            f"Não foi possível processar o arquivo: {erro}"
        )


else:

    st.info("Envie um CSV para começar.")