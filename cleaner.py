import pandas as pd

def remover_duplicatas(df: pd.DataFrame) -> pd.DataFrame:
    """Remove linhas completamente duplicadas."""

    # Remove as linhas repetidas e retorna uma cópia.
    return df.drop_duplicates().copy()


def limpar_espacos(df: pd.DataFrame) -> pd.DataFrame:
    """Remove espaços extras no início e no fim dos textos."""

    # Cria uma cópia para preservar os dados originais.
    df = df.copy()

    # Identifica somente as colunas que armazenam textos.
    colunas_texto = df.select_dtypes(
        include=["object", "string"]
    ).columns

    # Percorre as colunas e remove espaços nas extremidades.
    for coluna in colunas_texto:
        df[coluna] = df[coluna].str.strip()

    return df


def padronizar_vazios(df: pd.DataFrame) -> pd.DataFrame:
    """Converte textos vazios em valores ausentes."""

    # Cria uma cópia do DataFrame.
    df = df.copy()

    # Seleciona as colunas de texto.
    colunas_texto = df.select_dtypes(
        include=["object", "string"]
    ).columns

    # Substitui células vazias ou com apenas espaços por pd.NA.
    for coluna in colunas_texto:
        df[coluna] = df[coluna].replace(
            r"^\s*$", pd.NA, regex=True
        )

    return df


def limpar_csv(df: pd.DataFrame) -> pd.DataFrame:
    """Executa todas as regras básicas de limpeza."""

    # Aplica as regras em sequência.
    df_limpo = remover_duplicatas(df)
    df_limpo = limpar_espacos(df_limpo)
    df_limpo = padronizar_vazios(df_limpo)

    return df_limpo


def diagnostico_colunas(df: pd.DataFrame) -> pd.DataFrame:
    """Gera um diagnóstico de qualidade para cada coluna."""

    # Lista que armazenará os resultados.
    diagnostico = []

    # Percorre todas as colunas do arquivo.
    for coluna in df.columns:

        # Conta os valores ausentes.
        ausentes = int(df[coluna].isna().sum())

        # Calcula o percentual de valores ausentes.
        percentual_ausentes = (
            (ausentes / len(df)) * 100
            if len(df) > 0 else 0
        )

        # Conta os valores únicos, ignorando valores ausentes.
        valores_unicos = int(df[coluna].nunique())

        # Identifica o tipo de dado da coluna.
        tipo = str(df[coluna].dtype)

        # Armazena as informações encontradas.
        diagnostico.append({
            "Coluna": coluna,
            "Tipo de dado": tipo,
            "Valores únicos": valores_unicos,
            "Valores ausentes": ausentes,
            "% Ausentes": round(percentual_ausentes, 2)
        })

    # Converte a lista em um DataFrame.
    return pd.DataFrame(diagnostico)