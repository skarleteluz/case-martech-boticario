import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página e Identidade Visual (Cores Boticário)
st.set_page_config(page_title="Martech Analytics | Case Boticário", layout="wide")

# Estilo CSS para cores da marca
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    h1, h2, h3 { color: #004731; font-family: 'Arial'; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# 1. Carregamento e Processamento de Dados
@st.cache_data
def load_data():
    df = pd.read_csv('Case_Midia_Produto.csv')
    return df

df = load_data()

# Métricas consolidadas
df_canal = df.groupby('Canal').agg({
    'Investimento_Mkt': 'sum', 
    'Receita_Gerada': 'sum'
}).reset_index()
df_canal['ROAS'] = df_canal['Receita_Gerada'] / df_canal['Investimento_Mkt']

# ---------------------------------------------------------
# HEADER & KPIs
# ---------------------------------------------------------
st.title("📊 Análise de Performance: Campanhas de Inverno")
st.markdown("---")

col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
inv_total = df['Investimento_Mkt'].sum()
rec_total = df['Receita_Gerada'].sum()
roas_total = rec_total / inv_total

col_kpi1.metric("Investimento Total", f"R$ {inv_total:,.2f}")
col_kpi2.metric("Receita Gerada", f"R$ {rec_total:,.2f}")
col_kpi3.metric("ROAS Geral", f"{roas_total:.2f}x")
col_kpi4.metric("Status Meta Perfumaria", "Em Análise", delta_color="normal")

# ---------------------------------------------------------
# BLOCO 1: VISÃO GERAL DE CANAIS
# ---------------------------------------------------------
st.header("1. Eficiência Real por Canal")
col_graf1, col_text1 = st.columns([2, 1])

with col_graf1:
    # Combo Chart (Investimento vs ROAS)
    fig_combo = go.Figure()
    fig_combo.add_trace(go.Bar(x=df_canal['Canal'], y=df_canal['Investimento_Mkt'], name='Investimento (R$)', marker_color='#E2E2E2'))
    fig_combo.add_trace(go.Scatter(x=df_canal['Canal'], y=df_canal['ROAS'], name='ROAS', yaxis='y2', line=dict(color='#D4AF37', width=4)))
    
    fig_combo.update_layout(
        title="Onde estamos investindo vs. Onde temos retorno",
        yaxis=dict(title="Investimento (R$)"),
        yaxis2=dict(title="ROAS", overlaying='y', side='right'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="simple_white"
    )
    st.plotly_chart(fig_combo, use_container_width=True)

with col_text1:
    st.info("""
    **Principais Descobertas:**
    - O **Google Search** é o motor de rentabilidade da marca.
    - A **Mídia Programática** apresenta um ROAS de apenas 0.25, indicando que o tráfego barato não está a converter.
    """)

# ---------------------------------------------------------
# BLOCO 2: DEEP DIVE CATEGORIAS (O CORAÇÃO DO CASE)
# ---------------------------------------------------------
st.header("2. O Desafio da Perfumaria e Influenciadores")
col_graf2, col_graf3 = st.columns(2)

with col_graf2:
    # ROAS Perfumaria por Canal
    df_perf = df[df['Categoria_Anunciada'] == 'Perfumaria'].groupby('Canal').agg({'Investimento_Mkt': 'sum', 'Receita_Gerada': 'sum'}).reset_index()
    df_perf['ROAS'] = df_perf['Receita_Gerada'] / df_perf['Investimento_Mkt']
    
    fig_perf = px.bar(df_perf, x='Canal', y='ROAS', title="ROAS: Foco Perfumaria (Meta do Trimestre)",
                     color_discrete_sequence=['#004731'], text_auto='.2f')
    st.plotly_chart(fig_perf, use_container_width=True)
    st.caption("Nota: Influenciadores não se pagam em Perfumaria (ROAS < 1.0).")

with col_graf3:
    # Influenciadores por Categoria
    df_influ = df[df['Canal'] == 'Influenciadores'].groupby('Categoria_Anunciada').agg({'Investimento_Mkt': 'sum', 'Receita_Gerada': 'sum'}).reset_index()
    df_influ['ROAS'] = df_influ['Receita_Gerada'] / df_influ['Investimento_Mkt']
    
    fig_influ = px.bar(df_influ, x='Categoria_Anunciada', y='ROAS', title="Performance de Influenciadores por Categoria",
                      color_discrete_sequence=['#D4AF37'], text_auto='.2f')
    st.plotly_chart(fig_influ, use_container_width=True)
    st.caption("Influenciadores são altamente eficazes em Maquiagem.")

# ---------------------------------------------------------
# BLOCO 3: CONCLUSÃO E RECOMENDAÇÃO
# ---------------------------------------------------------
st.markdown("---")
st.header("3. Plano de Alocação: R$ 50.000 Extra")

# Criando 3 caixas de destaque
rec_col1, rec_col2, rec_col3 = st.columns(3)

with rec_col1:
    st.success("✅ **Prioridade 1: Google Search**")
    st.write("Alocação sugerida: **R$ 35.000**")
    st.write("Foco: Termos de fundo de funil para Perfumaria.")

with rec_col2:
    st.warning("📸 **Prioridade 2: Influenciadores**")
    st.write("Alocação sugerida: **R$ 10.000**")
    st.write("Foco: Campanhas de Maquiagem (ROAS 3.9x).")

with rec_col3:
    st.error("📉 **Prioridade 3: Programática**")
    st.write("Alocação sugerida: **R$ 5.000**")
    st.write("Foco: Apenas Remarketing de abandono de carrinho.")

st.balloons()
