"""
Testes básicos das funções de tratamento de dados.
Rodar com: pytest tests/
"""

import pandas as pd
import sys
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from data.load_data import clean_column_names


def test_clean_column_names():
    df = pd.DataFrame({
        "  Município ": [1, 2],
        "UF (Estado)": [3, 4],
    })
    df_clean = clean_column_names(df)

    assert "municipio" in df_clean.columns
    assert "uf_(estado)" in df_clean.columns
    assert all(" " not in col for col in df_clean.columns)