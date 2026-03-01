import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Funções auxiliares para formatação brasileira
def formata_br(valor, prefixo="R$ "):
    if pd.isna(valor): return "N/A"
    formatado = f"{valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    return f"{prefixo}{formatado}"

def formata_num(valor):
    return f"{valor:.2f}".replace(".", ",")

# Configuração da página e Identidade Visual
st.set_page_config(page_title="Martech Analytics | Case Boticário", layout="wide")

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

df = load_data()

# Métricas consolidadas
df_canal = df.groupby('Canal').agg({'Investimento_Mkt': 'sum', 'Receita_Gerada': 'sum'}).reset_index()
df_canal['ROAS'] = df_canal['Receita_Gerada'] / df_canal['Investimento_Mkt']

# ---------------------------------------------------------
# CABEÇALHO & KPIs
# ---------------------------------------------------------
st.title("📊 Dashboard de Performance: Campanhas de Inverno")
st.markdown("---")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
inv_total = df['Investimento_Mkt'].sum()
rec_total = df['Receita_Gerada'].sum()
roas_total = rec_total / inv_total

kpi1.metric("Investimento Total", formata_br(inv_total))
kpi2.metric("Receita Gerada", formata_br(rec_total))
kpi3.metric("ROAS Geral", f"{formata_num(roas_total)}x")
kpi4.metric("Status da Meta", "Foco Perfumaria")

# ---------------------------------------------------------
# BLOCO 1: VISÃO GERAL (CANAL E CATEGORIA LADO A LADO)
# ---------------------------------------------------------
st.header("1. Eficiência Real: Visão Comparativa")
col_canal, col_cat = st.columns(2)

with col_canal:
    # Gráfico por Canal
    fig_combo = go.Figure()
    fig_combo.add_trace(go.Bar(x=df_canal['Canal'], y=df_canal['Investimento_Mkt'], name='Investimento (R$)', marker_color='#E2E2E2'))
    fig_combo.add_trace(go.Scatter(x=df_canal['Canal'], y=df_canal['ROAS'], name='ROAS', yaxis='y2', line=dict(color='#D4AF37', width=4), marker=dict(size=10)))

    fig_combo.update_layout(
        title="Performance por Canal",
        yaxis=dict(title="Investimento (R$)"),
        yaxis2=dict(title="ROAS", overlaying='y', side='right'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="simple_white", separators=',.'
    )
    st.plotly_chart(fig_combo, use_container_width=True)

with col_cat:
    # Métricas por Categoria
    df_cat = df.groupby('Categoria_Anunciada').agg({'Investimento_Mkt': 'sum', 'Receita_Gerada': 'sum'}).reset_index()
    df_cat['ROAS'] = df_cat['Receita_Gerada'] / df_cat['Investimento_Mkt']
    
    # Gráfico por Categoria
    fig_cat = go.Figure()
    fig_cat.add_trace(go.Bar(x=df_cat['Categoria_Anunciada'], y=df_cat['Investimento_Mkt'], name='Investimento (R$)', marker_color='#E2E2E2'))
    fig_cat.add_trace(go.Scatter(x=df_cat['Categoria_Anunciada'], y=df_cat['ROAS'], name='ROAS', yaxis='y2', line=dict(color='#004731', width=4), marker=dict(size=10)))

    fig_cat.update_layout(
        title="Performance por Categoria",
        yaxis=dict(title="Investimento (R$)"),
        yaxis2=dict(title="ROAS", overlaying='y', side='right'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="simple_white", separators=',.'
    )
    st.plotly_chart(fig_cat, use_container_width=True)

# ---------------------------------------------------------
# NOVO BLOCO: MATRIZ DE PERFORMANCE (CANAL X CATEGORIA)
# ---------------------------------------------------------
st.header("2. Onde cada Canal brilha? (Afinidade)")

# Preparação dos dados agrupados por Canal e Categoria
df_matriz = df.groupby(['Canal', 'Categoria_Anunciada']).agg({
    'Investimento_Mkt': 'sum',
    'Receita_Gerada': 'sum'
}).reset_index()
df_matriz['ROAS'] = df_matriz['Receita_Gerada'] / df_matriz['Investimento_Mkt']

fig_matriz = px.bar(
    df_matriz, 
    x='Categoria_Anunciada', 
    y='ROAS', 
    color='Canal', 
    barmode='group',
    title='Comparativo de ROAS: Categorias por Canal de Mídia',
    color_discrete_map={
        'Google Search': '#004731',      # Verde Boticário
        'Influenciadores': '#D4AF37',    # Dourado
        'Programática': '#C0C0C0'        # Cinza
    },
    text_auto='.2f'
)

fig_matriz.update_layout(
    xaxis_title="Categoria do Produto",
    yaxis_title="ROAS (Eficiência)",
    legend_title="Canais",
    template="simple_white",
    separators=',.'
)

st.plotly_chart(fig_matriz, use_container_width=True)

st.info("""
**Análise da Matriz:**
- O **Google Search** domina a conversão em todas as categorias, especialmente em **Perfumaria**.
- **Influenciadores** mostram excelente performance em **Maquiagem**, mas enfrentam desafios em Perfumaria.
- A **Mídia Programática** tem uma performance linearmente baixa, sugerindo necessidade de revisão criativa ou de público.
""")

# ---------------------------------------------------------
# BLOCO 3: CONCLUSÃO E RECOMENDAÇÃO
# ---------------------------------------------------------
st.markdown("---")
st.header("3. Recomendação de Alocação: R$ 50.000 Extra")

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
