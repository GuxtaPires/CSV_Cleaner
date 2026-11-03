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
    """Converte textos vazios em valores ausentes."""
    df = df.copy()

    colunas_texto = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for coluna in colunas_texto:
        df[coluna] = df[coluna].replace(
            r"^\s*$", pd.NA, regex=True
        )

    return df


def limpar_csv(df: pd.DataFrame) -> pd.DataFrame:
    """Executa todas as regras básicas de limpeza."""
    df_limpo = remover_duplicatas(df)
    df_limpo = limpar_espacos(df_limpo)
    df_limpo = padronizar_vazios(df_limpo)

    return df_limpo


def diagnostico_colunas(df: pd.DataFrame) -> pd.DataFrame:
    """Gera um diagnóstico de qualidade para cada coluna."""
    diagnostico = []

    for coluna in df.columns:
        ausentes = int(df[coluna].isna().sum())

        percentual_ausentes = (
            (ausentes / len(df)) * 100
            if len(df) > 0 else 0
        )

        valores_unicos = int(df[coluna].nunique())
        tipo = str(df[coluna].dtype)

        diagnostico.append({
            "Coluna": coluna,
            "Tipo de dado": tipo,
            "Valores únicos": valores_unicos,
            "Valores ausentes": ausentes,
            "% Ausentes": round(percentual_ausentes, 2)
        })

    return pd.DataFrame(diagnostico)


def validar_coluna(
    df: pd.DataFrame,
    coluna: str,
    tipo_esperado: str
) -> dict:
    """Identifica valores incompatíveis com o tipo esperado."""

    valores_preenchidos = df[coluna].dropna()

    if tipo_esperado == "Numérico":
        convertidos = pd.to_numeric(
            valores_preenchidos,
            errors="coerce"
        )

    elif tipo_esperado == "Data":
        convertidos = pd.to_datetime(
            valores_preenchidos,
            errors="coerce"
        )

    else:
        raise ValueError("Tipo de validação não suportado.")

    mascara_invalidos = convertidos.isna()
    invalidos = valores_preenchidos[mascara_invalidos]

    tabela_invalidos = pd.DataFrame({
        "Índice original": invalidos.index,
        "Valor inválido": invalidos.astype(str).values
    })

    total = len(valores_preenchidos)
    quantidade_invalidos = int(mascara_invalidos.sum())

    return {
        "total": total,
        "validos": total - quantidade_invalidos,
        "invalidos": quantidade_invalidos,
        "percentual_invalidos": (
            round((quantidade_invalidos / total) * 100, 2)
            if total > 0 else 0
        ),
        "detalhes": tabela_invalidos
    }


def tratar_coluna(
    df: pd.DataFrame,
    coluna: str,
    tipo_esperado: str
) -> pd.DataFrame:
    """
    Converte uma coluna para o tipo selecionado.

    Valores incompatíveis são transformados em valores ausentes.
    O DataFrame original não é modificado.
    """

    # Trabalha sobre uma cópia dos dados.
    df_tratado = df.copy()

    # Converte a coluna para o tipo numérico.
    if tipo_esperado == "Numérico":

        df_tratado[coluna] = pd.to_numeric(
            df_tratado[coluna],
            errors="coerce"
        )

    # Converte a coluna para o formato de data.
    elif tipo_esperado == "Data":

        df_tratado[coluna] = pd.to_datetime(
            df_tratado[coluna],
            errors="coerce"
        )

    else:
        raise ValueError("Tipo de tratamento não suportado.")

    return df_tratado