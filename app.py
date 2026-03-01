import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuração da Página e Estilo Boticário
st.set_page_config(page_title="Martech Analytics | Grupo Boticário", layout="wide")

# CSS customizado para as cores da marca
st.markdown("""
    <style>
    .main { background-color: #F2F2F2; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #004731; }
    h1, h2, h3 { color: #004731; }
    </style>
    """, unsafe_allow_html=True)

# 2. Carregamento de Dados
@st.cache_data
def load_data():
    df = pd.read_csv('Case_Midia_Produto.csv')
    return df

df = load_data()

# Cálculos Base
df_canal = df.groupby('Canal').agg({'Investimento_Mkt': 'sum', 'Receita_Gerada': 'sum'}).reset_index()
df_canal['ROAS'] = df_canal['Receita_Gerada'] / df_canal['Investimento_Mkt']

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
st.sidebar.image("https://upload.wikimedia.org/wikipedia/pt/e/e0/Logotipo_do_Grupo_Botic%C3%A1rio.png", width=150)
st.sidebar.title("Martech Analytics")
st.sidebar.info("Análise de Performance: Campanhas de Inverno")

# ---------------------------------------------------------
# HEADER & KPIs
# ---------------------------------------------------------
st.title("📊 Dashboard de Performance de Mídia")
st.markdown("---")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
total_inv = df['Investimento_Mkt'].sum()
total_rec = df['Receita_Gerada'].sum()
total_roas = total_rec / total_inv

kpi1.metric("Investimento Total", f"R$ {total_inv:,.0f}")
kpi2.metric("Receita Gerada", f"R$ {total_rec:,.0f}")
kpi3.metric("ROAS Geral", f"{total_roas:.2f}x")
kpi4.metric("Canais Analisados", "3")

# ---------------------------------------------------------
# PERGUNTA 1: ROAS Real por Canal (Combo Chart)
# ---------------------------------------------------------
st.header("1. Eficiência por Canal (ROAS)")
col1, col2 = st.columns([2, 1])

with col1:
    fig_combo = go.Figure()
    fig_combo.add_trace(go.Bar(x=df_canal['Canal'], y=df_canal['Investimento_Mkt'], name='Investimento (R$)', marker_color='#E2E2E2'))
    fig_combo.add_trace(go.Scatter(x=df_canal['Canal'], y=df_canal['ROAS'], name='ROAS', yaxis='y2', line=dict(color='#D4AF37', width=4), marker=dict(size=10)))
    
    fig_combo.update_layout(
        title="Investimento vs. ROAS por Canal",
        yaxis=dict(title="Investimento (R$)"),
        yaxis2=dict(title="ROAS", overlaying='y', side='right'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_combo, use_container_width=True)

with col2:
    st.write("**Insight:**")
    st.write("""
    - O **Google Search** é o canal mais eficiente.
    - A **Mídia Programática** tem volume, mas a menor eficiência de conversão direta.
    """)

# ---------------------------------------------------------
# PERGUNTA 2 & 3: Foco Perfumaria e Influenciadores
# ---------------------------------------------------------
st.header("2. Deep Dive: Perfumaria & Influenciadores")
col3, col4 = st.columns(2)

with col3:
    # Filtro Perfumaria
    df_perf = df[df['Categoria_Anunciada'] == 'Perfumaria'].groupby('Canal').agg({'Investimento_Mkt': 'sum', 'Receita_Gerada': 'sum'}).reset_index()
    df_perf['ROAS'] = df_perf['Receita_Gerada'] / df_perf['Investimento_Mkt']
    
    fig_perf = px.bar(df_perf, x='Canal', y='ROAS', title="ROAS em Perfumaria (Meta do Trimestre)", 
                     color_discrete_sequence=['#004731'])
    st.plotly_chart(fig_perf, use_container_width=True)
    st.warning("Atenção: Influenciadores em Perfumaria operam com ROAS < 1.0 (0.84).")

with col4:
    # Influenciadores por Categoria
    df_influ = df[df['Canal'] == 'Influenciadores'].groupby('Categoria_Anunciada').agg({'Investimento_Mkt': 'sum', 'Receita_Gerada': 'sum'}).reset_index()
    df_influ['ROAS'] = df_influ['Receita_Gerada'] / df_influ['Investimento_Mkt']
    
    fig_influ = px.bar(df_influ, x='Categoria_Anunciada', y='ROAS', title="ROAS de Influenciadores por Categoria",
                      color_discrete_sequence=['#D4AF37'])
    st.plotly_chart(fig_influ, use_container_width=True)
    st.write("Influenciadores performam melhor em **Maquiagem** do que em Perfumaria.")

# ---------------------------------------------------------
# CONCLUSÃO: Onde investir os R$ 50.000?
# ---------------------------------------------------------
st.markdown("---")
st.header("3. Recomendação Final: Alocação de Verba Extra")

c1, c2, c3 = st.columns(3)
c1.success("🚀 **Google Search (70%)** \n Foco total em Perfumaria para bater a meta.")
c2.info("💄 **Influenciadores (25%)** \n Foco em Maquiagem (onde o canal se paga).")
c3.error("📉 **Programática (5%)** \n Redução de verba; manter apenas Remarketing.")

st.balloons()

