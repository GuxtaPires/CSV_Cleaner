import pandas as pd

def remover_duplicatas(df: pd.DataFrame) -> pd.DataFrame:
    """Remove linhas completamente duplicadas."""
    # Cria uma cópia do DataFrame sem linhas repetidas.
    # O copy() evita trabalhar diretamente sobre o objeto original.
    return df.drop_duplicates().copy()


def limpar_espacos(df: pd.DataFrame) -> pd.DataFrame:
    """Remove espaços extras no início e no fim dos textos."""
    # Cria uma cópia para preservar os dados recebidos.
    df = df.copy()

    # Seleciona apenas as colunas que armazenam textos.
    colunas_texto = df.select_dtypes(
        include=["object", "string"]
    ).columns

    # Percorre cada coluna de texto e remove espaços nas extremidades.
    for coluna in colunas_texto:
        df[coluna] = df[coluna].str.strip()

    # Retorna o DataFrame com os textos tratados.
    return df


def padronizar_vazios(df: pd.DataFrame) -> pd.DataFrame:
    """Converte textos vazios ou só com espaços em valores ausentes."""
    # Cria uma cópia para não modificar o DataFrame original.
    df = df.copy()

    # Identifica as colunas que armazenam textos.
    colunas_texto = df.select_dtypes(
        include=["object", "string"]
    ).columns

    # Substitui células vazias ou contendo apenas espaços por pd.NA.
    for coluna in colunas_texto:
        df[coluna] = df[coluna].replace(
            r"^\s*$", pd.NA, regex=True
        )

    # Retorna os dados após a padronização.
    return df


def limpar_csv(df: pd.DataFrame) -> pd.DataFrame:
    """Executa as regras básicas de limpeza."""
    # Remove duplicatas primeiro.
    df_limpo = remover_duplicatas(df)

    # Depois, remove espaços extras dos textos.
    df_limpo = limpar_espacos(df_limpo)

    # Por último, padroniza textos vazios como valores ausentes.
    df_limpo = padronizar_vazios(df_limpo)

    # Retorna o DataFrame após todas as etapas.
    return df_limpo