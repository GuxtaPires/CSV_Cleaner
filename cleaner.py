import pandas as pd

def remover_duplicatas(df: pd.DataFrame) -> pd.DataFrame:
    """Remove linhas completamente duplicadas."""
    return df.drop_duplicates().copy()


def limpar_espacos(df: pd.DataFrame) -> pd.DataFrame:
    """Remove espaços extras no início e no fim dos textos."""
    df = df.copy()

    colunas_texto = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for coluna in colunas_texto:
        df[coluna] = df[coluna].str.strip()

    return df


def padronizar_vazios(df: pd.DataFrame) -> pd.DataFrame:
    """Converte textos vazios ou só com espaços em valores ausentes."""
    df = df.copy()

    colunas_texto = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for coluna in colunas_texto:
        df[coluna] = df[coluna].replace(
            r"^\s*$",
            pd.NA,
            regex=True
        )

    return df


def limpar_csv(df: pd.DataFrame) -> pd.DataFrame:
    """Executa as regras básicas de limpeza."""
    df_limpo = remover_duplicatas(df)
    df_limpo = limpar_espacos(df_limpo)
    df_limpo = padronizar_vazios(df_limpo)

    return df_limpo