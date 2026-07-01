"""
Funções para carregar e tratar os dados de cobertura vacinal do DATASUS/TabNet.
"""

import pandas as pd
from pathlib import Path


def load_raw_csv(filepath: str, encoding: str = "latin1", sep: str = ";") -> pd.DataFrame:
    """
    Carrega um CSV bruto exportado do TabNet.

    O TabNet geralmente exporta em encoding latin1 e separador ';',
    com algumas linhas de cabeçalho/rodapé que precisam ser tratadas.

    Parameters
    ----------
    filepath : str
        Caminho do arquivo CSV bruto.
    encoding : str
        Encoding do arquivo (padrão do TabNet costuma ser latin1).
    sep : str
        Separador de colunas (padrão do TabNet costuma ser ';').

    Returns
    -------
    pd.DataFrame
        DataFrame com os dados brutos carregados.
    """
    df = pd.read_csv(filepath, encoding=encoding, sep=sep)
    return df


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Padroniza nomes de colunas: minúsculas, sem espaço, sem acento.
    """
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
        .str.replace(" ", "_")
    )
    return df


def save_processed(df: pd.DataFrame, filename: str, processed_dir: str = "data/processed") -> None:
    """
    Salva um DataFrame tratado na pasta de dados processados.
    """
    Path(processed_dir).mkdir(parents=True, exist_ok=True)
    output_path = Path(processed_dir) / filename
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Arquivo salvo em: {output_path}")