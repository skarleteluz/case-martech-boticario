import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- FUNÇÕES DE FORMATAÇÃO ---
def formata_br(valor, prefixo="R$ "):
    if pd.isna(valor): return "N/A"
    formatado = f"{valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    return f"{prefixo}{formatado}"

def formata_num(valor):
    return f"{valor:.2f}".replace(".", ",")

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Analytics Boticário", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    h1, h2, h3 { color: #004731; font-weight: bold; }
    .stMetric { background-color: #f9f9f9; border-left: 5px solid #004731; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('Case_Midia_Produto.csv')
    # Cálculo de ROAS por linha para o Treemap
    return df

df = load_data()

# --- CABEÇALHO ---
st.title("📊 Visão Estratégica: Spend vs. ROAS")
st.markdown("Análise multidimensional por Canal e Categoria de Produto.")

# KPIs Globais
m1, m2, m3 = st.columns(3)
inv_total = df['Investimento_Mkt'].sum()
rec_total = df['Receita_Gerada'].sum()
m1.metric("Spend Total", formata_br(inv_total))
m2.metric("Receita Total", formata_br(rec_total))
m3.metric("ROAS Global", f"{formata_num(rec_total/inv_total)}x")

st.markdown("---")

# --- O GRÁFICO PRINCIPAL: TREEMAP ---
st.header("1. Mapa de Oportunidades (Investimento e Eficiência)")

# Agrupando dados para a visão Canal > Categoria
df_tree = df.groupby(['Canal', 'Categoria_Anunciada']).agg({
    'Investimento_Mkt': 'sum',
    'Receita_Gerada': 'sum'
}).reset_index()
df_tree['ROAS'] = df_tree['Receita_Gerada'] / df_tree['Investimento_Mkt']

fig_tree = px.treemap(
    df_tree, 
    path=[px.Constant("Total"), 'Canal', 'Categoria_Anunciada'], 
    values='Investimento_Mkt',
    color='ROAS',
    color_continuous_scale=['#FF4B4B', '#F0F2F6', '#D4AF37', '#004731'], # Escala: Vermelho (Ruim) -> Dourado -> Verde (Bom)
    color_continuous_midpoint=1.0, # O ponto de equilíbrio (se paga)
    title="Tamanho do Bloco = Spend | Cor = ROAS",
    hover_data={'ROAS': ':.2f'}
)

fig_tree.update_layout(
    margin=dict(t=50, l=10, r=10, b=10),
    coloraxis_colorbar=dict(title="ROAS"),
    separators=',.'
)

st.plotly_chart(fig_tree, use_container_width=True)

st.info("""
**Como interpretar este gráfico:**
- **Áreas Verdes Grandes:** São nossos sucessos. Gastamos muito e o retorno é alto (ex: Google Search em Perfumaria).
- **Áreas Vermelhas/Cinzas Grandes:** São nossos pontos de atenção. Gastamos muito e o retorno é baixo (ex: Programática).
- **Blocos Pequenos e Verdes Escuros:** São oportunidades de escala. O ROAS é ótimo, mas o investimento ainda é baixo.
""")

# --- TABELA DE APOIO ---
st.header("2. Resumo Detalhado por Canal e Categoria")
df_table = df_tree.copy()
df_table['Spend'] = df_table['Investimento_Mkt'].apply(formata_br)
df_table['Receita'] = df_table['Receita_Gerada'].apply(formata_br)
df_table['ROAS (x)'] = df_table['ROAS'].apply(formata_num)

# Reorganizando colunas para a tabela
st.table(df_table[['Canal', 'Categoria_Anunciada', 'Spend', 'Receita', 'ROAS (x)']])

# --- RECOMENDAÇÃO ---
st.markdown("---")
st.header("3. Onde investir os R$ 50.000 extras?")
c1, c2, c3 = st.columns(3)
c1.success("**R$ 35.000 no Google Search**\n(Foco Perfumaria)")
c2.warning("**R$ 10.000 em Influenciadores**\n(Foco Maquiagem)")
c3.error("**R$ 5.000 em Programática**\n(Apenas Remarketing)")

st.balloons()
