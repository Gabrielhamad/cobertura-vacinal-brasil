import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import json
import urllib.request
import time

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="Cobertura Vacinal no Brasil",
    page_icon="💉",
    layout="wide"
)

# ============================================
# CSS CUSTOMIZADO (visual mais bonito)
# ============================================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }

    h1, h2, h3, p, span, label {
        color: #f0f0f0 !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #4ecdc4 !important;
    }

    [data-testid="stMetricLabel"] {
        color: #a0a0c0 !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        color: #f0f0f0;
    }

    .stTabs [aria-selected="true"] {
        background-color: rgba(78, 205, 196, 0.2);
        border-bottom: 3px solid #4ecdc4;
    }

    div[data-testid="stExpander"] {
        background-color: rgba(255, 255, 255, 0.03);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(78, 205, 196, 0.2);
        margin-bottom: 15px;
    }

    .big-number {
        font-size: 3rem;
        font-weight: 700;
        color: #4ecdc4;
        text-align: center;
    }

    .stAlert {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# CARREGAMENTO DE DADOS
# ============================================
@st.cache_data
def carregar_dados():
    df = pd.read_csv("data/processed/cobertura_vacinal_por_uf.csv")
    df_brasil = pd.read_csv("data/processed/cobertura_vacinal_brasil.csv")
    df_gasto = pd.read_csv("data/processed/gasto_saude_por_uf.csv")
    return df, df_brasil, df_gasto

df, df_brasil, df_gasto = carregar_dados()

dados_hesitacao = {
    "ano": [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
    "interesse": [3.50, 4.92, 5.33, 8.17, 9.92, 12.92, 10.75, 12.67, 54.58, 30.58]
}
df_hesitacao = pd.DataFrame(dados_hesitacao)

# Ajusta gráficos matplotlib para o tema escuro
plt.rcParams.update({
    "figure.facecolor": "none",
    "axes.facecolor": "none",
    "axes.edgecolor": "#a0a0c0",
    "axes.labelcolor": "#f0f0f0",
    "text.color": "#f0f0f0",
    "xtick.color": "#a0a0c0",
    "ytick.color": "#a0a0c0",
    "grid.color": "#3a3a5a",
    "legend.facecolor": "#1a1a2e",
    "legend.edgecolor": "#3a3a5a",
    "legend.labelcolor": "#f0f0f0",
})

# ============================================
# CABEÇALHO ANIMADO
# ============================================
st.markdown("""
<div style="text-align: center; padding: 20px 0;">
    <h1 style="font-size: 3rem; margin-bottom: 0;">💉 Cobertura Vacinal no Brasil</h1>
    <p style="font-size: 1.2rem; color: #a0a0c0;">2013 – 2022 · Investigando as causas por trás da queda pós-pandemia</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================
# FILTROS (SIDEBAR)
# ============================================
st.sidebar.markdown("## 🔎 Filtros")
vacina_selecionada = st.sidebar.selectbox("Vacina", sorted(df["vacina"].unique()))
anos_selecionados = st.sidebar.slider("Período", 2013, 2022, (2013, 2022))

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**📚 Fontes de dados**\n\n"
    "- DATASUS/TabNet (cobertura vacinal)\n"
    "- SIOPS (gasto em saúde)\n"
    "- Google Trends (hesitação vacinal)"
)
st.sidebar.markdown("[📂 Repositório no GitHub](https://github.com/Gabrielhamad/cobertura-vacinal-brasil)")

df_filtrado = df[
    (df["vacina"] == vacina_selecionada) &
    (df["ano"].between(anos_selecionados[0], anos_selecionados[1]))
]

# ============================================
# KPIs COM ANIMAÇÃO
# ============================================
col1, col2, col3, col4 = st.columns(4)

cobertura_2013 = df_filtrado[df_filtrado["ano"] == df_filtrado["ano"].min()]["cobertura"].mean()
cobertura_2022 = df_filtrado[df_filtrado["ano"] == df_filtrado["ano"].max()]["cobertura"].mean()
variacao = cobertura_2022 - cobertura_2013

with col1:
    st.metric("Cobertura Média", f"{df_filtrado['cobertura'].mean():.1f}%")
with col2:
    st.metric(
        f"Variação ({anos_selecionados[0]}→{anos_selecionados[1]})",
        f"{cobertura_2022:.1f}%",
        delta=f"{variacao:.1f} p.p."
    )
with col3:
    st.metric("🏆 Maior Cobertura", df_filtrado.groupby("uf")["cobertura"].mean().idxmax())
with col4:
    st.metric("⚠️ Menor Cobertura", df_filtrado.groupby("uf")["cobertura"].mean().idxmin())

st.markdown("---")

# ============================================
# ABAS
# ============================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📈  Evolução Temporal",
    "🗺️  Mapa por Estado",
    "💰  Hipótese: Investimento",
    "🔍  Hipótese: Hesitação Vacinal"
])

# --- ABA 1: EVOLUÇÃO TEMPORAL ---
with tab1:
    st.subheader(f"Evolução da Cobertura Vacinal — {vacina_selecionada}")

    fig, ax = plt.subplots(figsize=(11, 5))
    media_ano = df_filtrado.groupby("ano")["cobertura"].mean()
    ax.plot(media_ano.index, media_ano.values, marker="o", color="#4ecdc4", linewidth=3, markersize=8)
    ax.fill_between(media_ano.index, media_ano.values, alpha=0.15, color="#4ecdc4")
    ax.axhline(y=95, color="#ffd93d", linestyle="--", alpha=0.7, label="Meta ideal (95%)")
    ax.axvspan(2020, 2021, alpha=0.15, color="#ff6b6b", label="Período pandemia")
    ax.set_xlabel("Ano")
    ax.set_ylabel("Cobertura (%)")
    ax.legend()
    ax.grid(alpha=0.2)
    for spine in ax.spines.values():
        spine.set_visible(False)
    st.pyplot(fig)

    st.subheader("🏅 Ranking de Estados no Período")
    ranking = df_filtrado.groupby("uf")["cobertura"].mean().sort_values(ascending=False)
    st.bar_chart(ranking, color="#4ecdc4")

    with st.expander("📋 Ver dados detalhados"):
        st.dataframe(df_filtrado, use_container_width=True)

# --- ABA 2: MAPA ---
with tab2:
    st.subheader(f"Cobertura Vacinal por Estado — {vacina_selecionada} ({anos_selecionados[1]})")

    dados_mapa = (
        df[(df["vacina"] == vacina_selecionada) & (df["ano"] == anos_selecionados[1])]
        .groupby("uf")["cobertura"].mean().reset_index()
    )

    try:
        url_estados = "https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/brazil-states.geojson"
        with urllib.request.urlopen(url_estados, timeout=5) as response:
            geojson_brasil = json.loads(response.read())

        fig_mapa = px.choropleth(
            dados_mapa,
            geojson=geojson_brasil,
            locations="uf",
            featureidkey="properties.name",
            color="cobertura",
            color_continuous_scale="Teal",
            range_color=(dados_mapa["cobertura"].min() - 5, dados_mapa["cobertura"].max() + 5),
            scope="south america",
        )
        fig_mapa.update_geos(fitbounds="locations", visible=False)
        fig_mapa.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            height=500,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#f0f0f0"
        )
        st.plotly_chart(fig_mapa, use_container_width=True)
    except Exception:
        st.warning("Não foi possível carregar o mapa interativo. Exibindo ranking em tabela:")
        st.dataframe(dados_mapa.sort_values("cobertura", ascending=False), use_container_width=True)

# --- ABA 3: INVESTIMENTO ---
with tab3:
    st.subheader("💰 A queda foi causada por falta de investimento público?")
    st.markdown("### ❌ Hipótese refutada pelos dados")

    gasto_nacional = df_gasto.groupby("ano")["gasto_saude_per_capita"].mean().reset_index()
    cobertura_nacional = df_brasil.groupby("ano")["cobertura"].mean().reset_index()

    base_gasto = gasto_nacional["gasto_saude_per_capita"].iloc[0]
    base_cobertura = cobertura_nacional["cobertura"].iloc[0]
    gasto_nacional["indice"] = (gasto_nacional["gasto_saude_per_capita"] / base_gasto) * 100
    cobertura_nacional["indice"] = (cobertura_nacional["cobertura"] / base_cobertura) * 100

    fig2, ax2 = plt.subplots(figsize=(11, 5))
    ax2.plot(gasto_nacional["ano"], gasto_nacional["indice"], color="#ff6b6b", marker="o", linewidth=3, markersize=7, label="Gasto em saúde per capita")
    ax2.plot(cobertura_nacional["ano"], cobertura_nacional["indice"], color="#4ecdc4", marker="o", linewidth=3, markersize=7, label="Cobertura vacinal")
    ax2.axhline(y=100, color="#a0a0c0", linestyle="--", alpha=0.4)
    ax2.set_xlabel("Ano")
    ax2.set_ylabel("Índice (2013 = 100)")
    ax2.legend()
    ax2.grid(alpha=0.2)
    for spine in ax2.spines.values():
        spine.set_visible(False)
    st.pyplot(fig2)

    col_a, col_b = st.columns(2)
    col_a.metric("Correlação (nacional)", "-0,38")
    col_b.metric("Estados com correlação negativa", "26 de 26")

    st.info(
        "O gasto em saúde per capita subiu de forma consistente entre 2013 e 2022, "
        "enquanto a cobertura vacinal caiu — em todos os 26 estados analisados. "
        "Isso indica que o investimento público não parece ser a causa principal da queda."
    )

# --- ABA 4: HESITAÇÃO VACINAL ---
with tab4:
    st.subheader("🔍 A queda está associada à hesitação vacinal?")
    st.markdown("### ✅ Evidência forte de associação encontrada")

    col_c, col_d = st.columns(2)
    with col_c:
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        ax3.plot(cobertura_nacional["ano"], cobertura_nacional["cobertura"], color="#4ecdc4", marker="o", linewidth=2.5)
        ax3.fill_between(cobertura_nacional["ano"], cobertura_nacional["cobertura"], alpha=0.15, color="#4ecdc4")
        ax3.set_title("Cobertura Vacinal Nacional (%)")
        ax3.set_xlabel("Ano")
        ax3.grid(alpha=0.2)
        for spine in ax3.spines.values():
            spine.set_visible(False)
        st.pyplot(fig3)

    with col_d:
        fig4, ax4 = plt.subplots(figsize=(6, 4))
        ax4.plot(df_hesitacao["ano"], df_hesitacao["interesse"], color="#ff6b6b", marker="o", linewidth=2.5)
        ax4.fill_between(df_hesitacao["ano"], df_hesitacao["interesse"], alpha=0.15, color="#ff6b6b")
        ax4.set_title('Busca por "vacina faz mal" (Google Trends)')
        ax4.set_xlabel("Ano")
        ax4.grid(alpha=0.2)
        for spine in ax4.spines.values():
            spine.set_visible(False)
        st.pyplot(fig4)

    col_e, col_f, col_g = st.columns(3)
    col_e.metric("Correlação", "-0,76")
    col_f.metric("R² (regressão)", "0,579")
    col_g.metric("P-valor", "0,011")

    st.success(
        "O interesse de busca por termos como \"vacina faz mal\" explica quase 58% da variação "
        "na cobertura vacinal nacional, com significância estatística confirmada. "
        "Entre os fatores testados neste projeto, foi o que apresentou a associação mais forte — "
        "embora, por se tratar de dados observacionais, não seja possível afirmar causalidade."
    )

# ============================================
# RODAPÉ
# ============================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #a0a0c0; padding: 10px 0;">
    Projeto de análise de dados desenvolvido em Python (Pandas, Matplotlib, Plotly, Statsmodels) e SQL.
    <br>Código completo disponível no
    <a href="https://github.com/Gabrielhamad/cobertura-vacinal-brasil" style="color: #4ecdc4;">GitHub</a>.
</div>
""", unsafe_allow_html=True)