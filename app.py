import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- FUNÇÕES DE FORMATAÇÃO (PADRÃO BRASILEIRO) ---
def formata_br(valor, prefixo="R$ "):
    if pd.isna(valor): return "N/A"
    # Formatação de milhar com ponto e decimal com vírgula
    formatado = f"{valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    return f"{prefixo}{formatado}"

def formata_num(valor):
    # Formata apenas o número com vírgula decimal
    return f"{valor:.2f}".replace(".", ",")

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Analytics Grupo Boticário", layout="wide")

# Estilo visual Boticário
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    h1, h2, h3 { color: #004731; font-family: 'Arial'; }
    .stMetric { border-left: 5px solid #004731; background-color: #f9f9f9; padding: 20px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    # O arquivo CSV deve estar na mesma pasta do script
    return pd.read_csv('Case_Midia_Produto.csv')

df = load_data()

# --- CABEÇALHO ---
st.title("📊 Relatório de Performance: Campanhas de Inverno")
st.markdown("Análise de eficiência cruzada para suporte à decisão de alocação de verba extra.")
st.markdown("---")

# KPIs de Resumo no Topo
k1, k2, k3 = st.columns(3)
inv_total = df['Investimento_Mkt'].sum()
rec_total = df['Receita_Gerada'].sum()
roas_global = rec_total / inv_total

k1.metric("Investimento Total (Spend)", formata_br(inv_total))
k2.metric("Receita Total Gerada", formata_br(rec_total))
k3.metric("ROAS Global", f"{formata_num(roas_global)}x")

# --- SEÇÃO 1: EFICIÊNCIA POR CANAL ---
st.header("1. Eficiência Real por Canal")
df_canal = df.groupby('Canal').agg({'Investimento_Mkt': 'sum', 'Receita_Gerada': 'sum'}).reset_index()
df_canal['ROAS'] = df_canal['Receita_Gerada'] / df_canal['Investimento_Mkt']

fig_canal = go.Figure()
fig_canal.add_trace(go.Bar(x=df_canal['Canal'], y=df_canal['Investimento_Mkt'], name='Investimento (R$)', marker_color='#E2E2E2'))
fig_canal.add_trace(go.Scatter(x=df_canal['Canal'], y=df_canal['ROAS'], name='ROAS', yaxis='y2', line=dict(color='#D4AF37', width=4), marker=dict(size=10)))

fig_canal.update_layout(
    title="Visão por Canal: Gasto vs. ROAS",
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

col_graf_cat, col_insight_cat = st.columns([2, 1])

with col_graf_cat:
    fig_cat = go.Figure()
    fig_cat.add_trace(go.Bar(x=df_cat['Categoria_Anunciada'], y=df_cat['Investimento_Mkt'], name='Investimento (R$)', marker_color='#E2E2E2'))
    fig_cat.add_trace(go.Scatter(x=df_cat['Categoria_Anunciada'], y=df_cat['ROAS'], name='ROAS', yaxis='y2', line=dict(color='#004731', width=4), marker=dict(size=10)))

    fig_cat.update_layout(
        title="Visão por Categoria: Gasto vs. ROAS",
        yaxis=dict(title="Investimento (R$)"),
        yaxis2=dict(title="ROAS", overlaying='y', side='right'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="simple_white", separators=',.'
    )
    st.plotly_chart(fig_cat, use_container_width=True)

with col_insight_cat:
    st.markdown(f"""
    ### 💡 Racional de Portfólio
    A categoria de **Perfumaria** não é apenas o foco do trimestre, é o ativo de **maior rentabilidade** do portfólio atual.
    
    * **Meta de Negócio:** Enquanto Maquiagem e Cabelos operam com ROAS saudáveis, a Perfumaria entrega a maior eficiência sobre o capital investido.
    * **Poder de Tração:** Isso justifica o direcionamento majoritário da verba extra, pois a categoria possui a melhor resposta financeira imediata.
    """)

# --- SEÇÃO 3: CRUZAMENTO (CANAL X CATEGORIA) ---
st.header("3. Cruzamento Detalhado: Onde cada canal brilha?")
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

# --- SEÇÃO 4: RECOMENDAÇÃO FINAL (EXATAMENTE COMO VOCÊ PEDIU) ---
st.markdown("---")
st.header("4. Recomendação de Alocação: R$ 50.000 Extra")

rec_col1, rec_col2, rec_col3 = st.columns(3)

with rec_col1:
    st.success("🚀 **Prioridade 1: Google Search**")
    st.write(f"Alocação sugerida: **{formata_br(35000)}**")
    st.write(f"Foco: Perfumaria (ROAS {formata_num(9.86)}x).")

with rec_col2:
    st.warning("📸 **Prioridade 2: Influenciadores**")
    st.write(f"Alocação sugerida: **{formata_br(10000)}**")
    st.write(f"Foco: Maquiagem (ROAS {formata_num(3.99)}x).")

with rec_col3:
    st.error("📉 **Prioridade 3: Programática**")
    st.write(f"Alocação sugerida: **{formata_br(5000)}**")
    st.write("Foco: Remarketing de fundo de funil.")

st.balloons()




