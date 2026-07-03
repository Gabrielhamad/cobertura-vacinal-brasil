import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Cobertura Vacinal no Brasil", layout="wide")

st.title("💉 Cobertura Vacinal no Brasil (2013-2022)")
st.markdown("Análise interativa da evolução da cobertura vacinal e seus fatores associados.")

# Carrega os dados
df = pd.read_csv("data/processed/cobertura_vacinal_por_uf.csv")
df_brasil = pd.read_csv("data/processed/cobertura_vacinal_brasil.csv")

# Filtros na barra lateral
st.sidebar.header("Filtros")
vacina_selecionada = st.sidebar.selectbox("Vacina", df["vacina"].unique())
anos_selecionados = st.sidebar.slider("Período", 2013, 2022, (2013, 2022))

# Filtra os dados
df_filtrado = df[
    (df["vacina"] == vacina_selecionada) &
    (df["ano"].between(anos_selecionados[0], anos_selecionados[1]))
]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Cobertura Média", f"{df_filtrado['cobertura'].mean():.1f}%")
col2.metric("Estado com Maior Cobertura", df_filtrado.groupby("uf")["cobertura"].mean().idxmax())
col3.metric("Estado com Menor Cobertura", df_filtrado.groupby("uf")["cobertura"].mean().idxmin())

# Gráfico de evolução
st.subheader(f"Evolução da Cobertura — {vacina_selecionada}")
fig, ax = plt.subplots(figsize=(10, 4))
media_ano = df_filtrado.groupby("ano")["cobertura"].mean()
ax.plot(media_ano.index, media_ano.values, marker="o", color="steelblue", linewidth=2.5)
ax.axhline(y=95, color="gray", linestyle="--", alpha=0.5)
ax.set_xlabel("Ano")
ax.set_ylabel("Cobertura (%)")
ax.grid(alpha=0.3)
st.pyplot(fig)

# Ranking de estados
st.subheader("Ranking de Estados")
ranking = df_filtrado.groupby("uf")["cobertura"].mean().sort_values(ascending=False)
st.bar_chart(ranking)

# Tabela de dados
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)