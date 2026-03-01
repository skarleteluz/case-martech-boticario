import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- FUNÇÕES AUXILIARES DE FORMATAÇÃO (PADRÃO BRASILEIRO) ---
def formata_br(valor, prefixo="R$ "):
    if pd.isna(valor): return "N/A"
    formatado = f"{valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    return f"{prefixo}{formatado}"

def formata_num(valor):
    return f"{valor:.2f}".replace(".", ",")

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Martech Analytics | Grupo Boticário", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    h1, h2, h3 { color: #004731; font-family: 'Arial'; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); border-left: 5px solid #004731; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('Case_Midia_Produto.csv')
    return df

df_raw = load_data()

# --- SIDEBAR (FILTROS) ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/pt/e/e0/Logotipo_do_Grupo_Botic%C3%A1rio.png", width=150)
st.sidebar.title("Filtros Estratégicos")

canais_selecionados = st.sidebar.multiselect(
    "Selecione os Canais:",
    options=df_raw['Canal'].unique(),
    default=df_raw['Canal'].unique()
)

categorias_selecionadas = st.sidebar.multiselect(
    "Selecione as Categorias:",
    options=df_raw['Categoria_Anunciada'].unique(),
    default=df_raw['Categoria_Anunciada'].unique()
)

# Aplicando os Filtros
df = df_raw[
    (df_raw['Canal'].isin(canais_selecionados)) & 
    (df_raw['Categoria_Anunciada'].isin(categorias_selecionadas))
]

# --- DASHBOARD PRINCIPAL ---
st.title("📊 Resumo Visual: Spend, Receita e ROAS")
st.markdown("Analise a performance cruzando canais e categorias de produtos.")

# --- KPIs DINÂMICOS ---
kpi1, kpi2, kpi3 = st.columns(3)
inv_total = df['Investimento_Mkt'].sum()
rec_total = df['Receita_Gerada'].sum()
roas_total = rec_total / inv_total if inv_total > 0 else 0

kpi1.metric("Investimento (Spend)", formata_br(inv_total))
kpi2.metric("Receita Gerada", formata_br(rec_total))
kpi3.metric("ROAS Atual", f"{formata_num(roas_total)}x")

st.markdown("---")

# --- GRÁFICO 1: SPEND E RECEITA POR CANAL/CATEGORIA ---
st.header("1. Visão de Investimento (Spend) vs. Receita")
col1, col2 = st.columns([2, 1])

with col1:
    # Agrupando dados para o gráfico de barras
    df_grouped = df.groupby(['Canal', 'Categoria_Anunciada']).agg({
        'Investimento_Mkt': 'sum',
        'Receita_Gerada': 'sum'
    }).reset_index()

    # Melt para facilitar a visualização de barras lado a lado
    df_melted = df_grouped.melt(id_vars=['Canal', 'Categoria_Anunciada'], 
                                value_vars=['Investimento_Mkt', 'Receita_Gerada'],
                                var_name='Métrica', value_name='Valor')
    
    df_melted['Métrica'] = df_melted['Métrica'].replace({'Investimento_Mkt': 'Spend (Investimento)', 'Receita_Gerada': 'Receita'})

    fig_barras = px.bar(
        df_melted, 
        x='Canal', 
        y='Valor', 
        color='Métrica', 
        barmode='group',
        facet_col='Categoria_Anunciada',
        color_discrete_map={'Spend (Investimento)': '#C0C0C0', 'Receita': '#004731'},
        template="simple_white"
    )
    fig_barras.update_layout(separators=',.')
    st.plotly_chart(fig_barras, use_container_width=True)

with col2:
    st.write("**Entenda a Visão:**")
    st.write("""
    Este gráfico compara o quanto estamos gastando (*Spend*) versus o quanto estamos faturando por cada categoria. 
    
    Use os filtros laterais para isolar uma categoria específica (ex: Perfumaria) e ver o comportamento dos canais nela.
    """)

# --- GRÁFICO 2: MAPA DE CALOR DO ROAS (O DETALHE DO CASE) ---
st.header("2. Eficiência Detalhada (ROAS)")

df_grouped['ROAS'] = df_grouped['Receita_Gerada'] / df_grouped['Investimento_Mkt']

fig_roas = px.bar(
    df_grouped, 
    x='Categoria_Anunciada', 
    y='ROAS', 
    color='Canal', 
    barmode='group',
    text_auto='.2f',
    color_discrete_map={'Google Search': '#004731', 'Influenciadores': '#D4AF37', 'Programática': '#76933C'},
    template="simple_white"
)
fig_roas.update_layout(separators=',.')
st.plotly_chart(fig_roas, use_container_width=True)

# --- TABELA DE APOIO (PARA EXPORTAÇÃO OU AUDITORIA) ---
with st.expander("Ver Tabela de Dados Detalhada"):
    df_table = df_grouped.copy()
    df_table['Investimento_Mkt'] = df_table['Investimento_Mkt'].apply(formata_br)
    df_table['Receita_Gerada'] = df_table['Receita_Gerada'].apply(formata_br)
    df_table['ROAS'] = df_table['ROAS'].apply(formata_num)
    st.table(df_table)

st.balloons()
