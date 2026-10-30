import pandas as pd


def remover_duplicatas(df: pd.DataFrame) -> pd.DataFrame:
    """Remove linhas completamente duplicadas."""

    return df.drop_duplicates().copy()


def limpar_espacos(df: pd.DataFrame) -> pd.DataFrame:
    """Remove espaços extras no início e no fim dos textos."""

    df = df.copy()

    # Seleciona somente as colunas de texto.
    colunas_texto = df.select_dtypes(
        include=["object", "string"]
    ).columns

    # Remove espaços das extremidades.
    for coluna in colunas_texto:
        df[coluna] = df[coluna].str.strip()

    return df


def padronizar_vazios(df: pd.DataFrame) -> pd.DataFrame:
    """Converte textos vazios em valores ausentes."""

    df = df.copy()

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

    df_limpo = remover_duplicatas(df)
    df_limpo = limpar_espacos(df_limpo)
    df_limpo = padronizar_vazios(df_limpo)

    return df_limpo


def diagnostico_colunas(df: pd.DataFrame) -> pd.DataFrame:
    """Gera um diagnóstico de qualidade para cada coluna."""

    diagnostico = []

    for coluna in df.columns:

        # Conta valores ausentes.
        ausentes = int(df[coluna].isna().sum())

        # Calcula o percentual de valores ausentes.
        percentual_ausentes = (
            (ausentes / len(df)) * 100
            if len(df) > 0 else 0
        )

        # Conta valores únicos, ignorando ausentes.
        valores_unicos = int(df[coluna].nunique())

        # Identifica o tipo de dado.
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
    """
    Valida uma coluna conforme o tipo esperado.

    Retorna a quantidade de valores válidos,
    inválidos e uma tabela com os valores problemáticos.
    """

    # Recupera a coluna selecionada.
    serie = df[coluna]

    # Ignora valores que já estão ausentes.
    valores_preenchidos = serie.dropna()

    # Validação numérica.
    if tipo_esperado == "Numérico":

        # Tenta converter os valores para números.
        convertidos = pd.to_numeric(
            valores_preenchidos,
            errors="coerce"
        )

    # Validação de datas.
    elif tipo_esperado == "Data":

        # Tenta interpretar os valores como datas.
        convertidos = pd.to_datetime(
            valores_preenchidos,
            errors="coerce"
        )

    else:
        raise ValueError("Tipo de validação não suportado.")

    # Identifica os valores que não puderam ser convertidos.
    mascara_invalidos = convertidos.isna()

    # Recupera os valores inválidos e seus índices originais.
    invalidos = valores_preenchidos[mascara_invalidos]

    # Monta uma tabela com os valores problemáticos.
    tabela_invalidos = pd.DataFrame({
        "Índice original": invalidos.index,
        "Valor inválido": invalidos.astype(str).values
    })

    # Retorna o resultado da validação.
    return {
        "total": len(valores_preenchidos),
        "validos": int((~mascara_invalidos).sum()),
        "invalidos": int(mascara_invalidos.sum()),
        "percentual_invalidos": (
            round(
                (mascara_invalidos.sum() / len(valores_preenchidos)) * 100,
                2
            )
            if len(valores_preenchidos) > 0 else 0
        ),
        "detalhes": tabela_invalidos
    }