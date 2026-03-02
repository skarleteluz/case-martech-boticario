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

# ---------------------------------------------------------
# NAVEGAÇÃO LATERAL
# ---------------------------------------------------------
st.sidebar.title("Navegação")
pagina = st.sidebar.radio("Selecione a visualização:", ["Visão Geral", "Análise por Canal (Deep Dive)"])

# ---------------------------------------------------------
# PÁGINA 1: VISÃO GERAL (SEU CÓDIGO ORIGINAL)
# ---------------------------------------------------------
if pagina == "Visão Geral":
    # Métricas consolidadas
    df_canal = df.groupby('Canal').agg({'Investimento_Mkt': 'sum', 'Receita_Gerada': 'sum'}).reset_index()
    df_canal['ROAS'] = df_canal['Receita_Gerada'] / df_canal['Investimento_Mkt']

    st.title("📊 Dashboard de Performance: Campanhas de Inverno")
    st.markdown("---")

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    inv_total = df['Investimento_Mkt'].sum()
    rec_total = df['Receita_Gerada'].sum()
    roas_total = rec_total / inv_total

    kpi1.metric("Investimento Total", formata_br(inv_total))
    kpi2.metric("Receita Gerada", formata_br(rec_total))
    kpi3.metric("ROAS Geral", f"{formata_num(roas_total)}x")
    kpi4.metric("Meta", "Perfumaria")

    st.header("1. Eficiência Real: Visão Comparativa")
    col_canal, col_cat = st.columns(2)

    with col_canal:
        fig_combo = go.Figure()
        fig_combo.add_trace(go.Bar(x=df_canal['Canal'], y=df_canal['Investimento_Mkt'], name='Investimento (R$)', marker_color='#E2E2E2'))
        fig_combo.add_trace(go.Scatter(x=df_canal['Canal'], y=df_canal['ROAS'], name='ROAS', yaxis='y2', line=dict(color='#D4AF37', width=4), marker=dict(size=10)))
        fig_combo.update_layout(title="Performance por Canal", yaxis=dict(title="Investimento (R$)"), yaxis2=dict(title="ROAS", overlaying='y', side='right'), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), template="simple_white", separators=',.')
        st.plotly_chart(fig_combo, use_container_width=True)

    with col_cat:
        df_cat = df.groupby('Categoria_Anunciada').agg({'Investimento_Mkt': 'sum', 'Receita_Gerada': 'sum'}).reset_index()
        df_cat['ROAS'] = df_cat['Receita_Gerada'] / df_cat['Investimento_Mkt']
        fig_cat = go.Figure()
        fig_cat.add_trace(go.Bar(x=df_cat['Categoria_Anunciada'], y=df_cat['Investimento_Mkt'], name='Investimento (R$)', marker_color='#E2E2E2'))
        fig_cat.add_trace(go.Scatter(x=df_cat['Categoria_Anunciada'], y=df_cat['ROAS'], name='ROAS', yaxis='y2', line=dict(color='#D4AF37', width=4), marker=dict(size=10)))
        fig_cat.update_layout(title="Performance por Categoria", yaxis=dict(title="Investimento (R$)"), yaxis2=dict(title="ROAS", overlaying='y', side='right'), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), template="simple_white", separators=',.')
        st.plotly_chart(fig_cat, use_container_width=True)

    st.header("2. Onde cada Canal Performa Melhor?)")
    df_matriz = df.groupby(['Canal', 'Categoria_Anunciada']).agg({'Investimento_Mkt': 'sum', 'Receita_Gerada': 'sum'}).reset_index()
    df_matriz['ROAS'] = df_matriz['Receita_Gerada'] / df_matriz['Investimento_Mkt']
    fig_matriz = px.bar(df_matriz, x='Categoria_Anunciada', y='ROAS', color='Canal', barmode='group', title='Comparativo de ROAS: Categorias por Canal de Mídia', color_discrete_map={'Google Search': '#004731', 'Influenciadores': '#D4AF37', 'Programática': '#C0C0C0'}, text_auto='.2f')
    fig_matriz.update_layout(xaxis_title="Categoria do Produto", yaxis_title="ROAS (Eficiência)", legend_title="Canais", template="simple_white", separators=',.')
    st.plotly_chart(fig_matriz, use_container_width=True)

    st.info("""
    **Análise da Matriz:**
    - O **Google Search** domina a conversão em todas as categorias, especialmente em **Perfumaria**.
    - **Influenciadores** mostram excelente performance em **Maquiagem**, mas enfrentam desafios em Perfumaria.
    - A **Mídia Programática** tem uma performance linearmente baixa, sugerindo necessidade de revisão criativa ou de público.
    """)

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

# ---------------------------------------------------------
# PÁGINA 2: DEEP DIVE POR CANAL (NOVA PÁGINA)
# ---------------------------------------------------------
else:
    st.title("🔍 Análise Detalhada por Canal")
    st.markdown("---")

    # Seletor de Canal
    lista_canais = df['Canal'].unique().tolist()
    canal_selecionado = st.selectbox("Escolha o Canal de Mídia para auditar:", lista_canais)

    # Filtragem dos dados
    df_filtrado = df[df['Canal'] == canal_selecionado]
    
    # Métricas do Canal
    inv_canal = df_filtrado['Investimento_Mkt'].sum()
    rec_canal = df_filtrado['Receita_Gerada'].sum()
    roas_canal = rec_canal / inv_canal if inv_canal > 0 else 0

    c1, c2, c3 = st.columns(3)
    c1.metric(f"Investimento em {canal_selecionado}", formata_br(inv_canal))
    c2.metric(f"Receita em {canal_selecionado}", formata_br(rec_canal))
    c3.metric(f"ROAS Geral do Canal", f"{formata_num(roas_canal)}x")

    st.markdown("---")
    
    # Gráfico de Investimento por Categoria dentro do Canal
    st.subheader(f"Distribuição de Verba por Categoria: {canal_selecionado}")
    
    df_cat_canal = df_filtrado.groupby('Categoria_Anunciada').agg({
        'Investimento_Mkt': 'sum',
        'Receita_Gerada': 'sum'
    }).reset_index()
    df_cat_canal['ROAS'] = df_cat_canal['Receita_Gerada'] / df_cat_canal['Investimento_Mkt']

    # Criando gráfico de barras para investimento
    fig_deep = px.bar(
        df_cat_canal,
        x='Categoria_Anunciada',
        y='Investimento_Mkt',
        text='Investimento_Mkt',
        labels={'Investimento_Mkt': 'Investimento (R$)', 'Categoria_Anunciada': 'Categoria'},
        color='Categoria_Anunciada',
        color_discrete_map={'Perfumaria': '#004731', 'Maquiagem': '#D4AF37', 'Cabelos': '#7A7A7A'}
    )
    
    fig_deep.update_traces(texttemplate='R$ %{text:.2s}', textposition='outside')
    fig_deep.update_layout(template="simple_white", showlegend=False)
    
    st.plotly_chart(fig_deep, use_container_width=True)

    # Tabela de apoio com ROAS por categoria naquele canal
    st.write(f"**Performance Detalhada de {canal_selecionado}:**")
    
    # Formatação para exibição na tabela
    df_tabela = df_cat_canal.copy()
    df_tabela['Investimento_Mkt'] = df_tabela['Investimento_Mkt'].apply(formata_br)
    df_tabela['Receita_Gerada'] = df_tabela['Receita_Gerada'].apply(formata_br)
    df_tabela['ROAS'] = df_tabela['ROAS'].apply(lambda x: f"{formata_num(x)}x")
    
    st.table(df_tabela[['Categoria_Anunciada', 'Investimento_Mkt', 'Receita_Gerada', 'ROAS']])

    if canal_selecionado == "Influenciadores":
        st.warning("⚠️ **Observação Crítica:** Note que a categoria 'Cabelos' consome uma verba significativa neste canal, mas o retorno (ROAS) é o mais baixo observado.")
