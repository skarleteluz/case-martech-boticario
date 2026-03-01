import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- FUNÇÕES DE FORMATAÇÃO (PADRÃO BRASILEIRO) ---
def formata_br(valor, prefixo="R$ "):
    if pd.isna(valor): return "N/A"
    formatado = f"{valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    return f"{prefixo}{formatado}"

def formata_num(valor):
    return f"{valor:.2f}".replace(".", ",")

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Analytics Grupo Boticário", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    h1, h2, h3 { color: #004731; font-family: 'Arial'; }
    .stMetric { border-left: 5px solid #004731; background-color: #f9f9f9; padding: 20px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv('Case_Midia_Produto.csv')

df = load_data()

# --- HEADER ---
st.image("https://upload.wikimedia.org/wikipedia/pt/e/e0/Logotipo_do_Grupo_Botic%C3%A1rio.png", width=200)
st.title("📊 Relatório de Performance: Campanhas de Inverno")
st.markdown("---")

# KPIs de Resumo
k1, k2, k3 = st.columns(3)
inv_total = df['Investimento_Mkt'].sum()
rec_total = df['Receita_Gerada'].sum()
k1.metric("Investimento Total (Spend)", formata_br(inv_total))
k2.metric("Receita Total Gerada", formata_br(rec_total))
k3.metric("ROAS Global", f"{formata_num(rec_total/inv_total)}x")

# --- SEÇÃO 1: EFICIÊNCIA POR CANAL ---
st.header("1. Eficiência Real por Canal")
df_canal = df.groupby('Canal').agg({'Investimento_Mkt': 'sum', 'Receita_Gerada': 'sum'}).reset_index()
df_canal['ROAS'] = df_canal['Receita_Gerada'] / df_canal['Investimento_Mkt']

fig_canal = go.Figure()
fig_canal.add_trace(go.Bar(x=df_canal['Canal'], y=df_canal['Investimento_Mkt'], name='Investimento (R$)', marker_color='#E2E2E2'))
fig_canal.add_trace(go.Scatter(x=df_canal['Canal'], y=df_canal['ROAS'], name='ROAS', yaxis='y2', line=dict(color='#D4AF37', width=4), marker=dict(size=10)))

fig_canal.update_layout(
    title="Investimento vs. ROAS por Canal",
    yaxis=dict(title="Investimento (R$)"),
    yaxis2=dict(title="ROAS", overlaying='y', side='right'),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    template="simple_white", separators=',.'
)
st.plotly_chart(fig_canal, use_container_width=True)

# --- SEÇÃO 2: EFICIÊNCIA POR CATEGORIA ---
st.header("2. Eficiência Real por Categoria")
df_cat = df.groupby('Categoria_Anunciada').agg({'Investimento_Mkt': 'sum', 'Receita_Gerada': 'sum'}).reset_index()
df_cat['ROAS'] = df_cat['Receita_Gerada'] / df_cat['Investimento_Mkt']

fig_cat = go.Figure()
fig_cat.add_trace(go.Bar(x=df_cat['Categoria_Anunciada'], y=df_cat['Investimento_Mkt'], name='Investimento (R$)', marker_color='#E2E2E2'))
fig_cat.add_trace(go.Scatter(x=df_cat['Categoria_Anunciada'], y=df_cat['ROAS'], name='ROAS', yaxis='y2', line=dict(color='#004731', width=4), marker=dict(size=10)))

fig_cat.update_layout(
    title="Investimento vs. ROAS por Categoria de Produto",
    yaxis=dict(title="Investimento (R$)"),
    yaxis2=dict(title="ROAS", overlaying='y', side='right'),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    template="simple_white", separators=',.'
)
st.plotly_chart(fig_cat, use_container_width=True)

# --- SEÇÃO 3: CRUZAMENTO E AFINIDADE ---
st.header("3. Cruzamento: Canal x Categoria")
df_matriz = df.groupby(['Canal', 'Categoria_Anunciada']).agg({'Investimento_Mkt': 'sum', 'Receita_Gerada': 'sum'}).reset_index()
df_matriz['ROAS'] = df_matriz['Receita_Gerada'] / df_matriz['Investimento_Mkt']

fig_matriz = px.bar(
    df_matriz, x='Categoria_Anunciada', y='ROAS', color='Canal', barmode='group',
    title='Comparativo de ROAS por Segmento',
    color_discrete_map={'Google Search': '#004731', 'Influenciadores': '#D4AF37', 'Programática': '#C0C0C0'},
    text_auto='.2f'
)
fig_matriz.update_layout(template="simple_white", separators=',.')
st.plotly_chart(fig_matriz, use_container_width=True)

# --- RECOMENDAÇÃO FINAL ---
st.markdown("---")
st.header("4. Recomendação de Alocação (R$ 50.000 Extra)")
c1, c2, c3 = st.columns(3)
c1.success("**70% no Google Search**\n\nFoco em Perfumaria. ROAS histórico de 9,86x.")
c2.warning("**20% em Influenciadores**\n\nFoco em Maquiagem. ROAS histórico de 3,99x.")
c3.error("**10% em Programática**\n\nManter apenas para Remarketing de fundo de funil.")

st.balloons()
