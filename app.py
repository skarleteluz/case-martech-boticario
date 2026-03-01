import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Função auxiliar para formatação brasileira (milhar com ponto, decimal com vírgula)
def formata_br(valor, prefixo="R$ "):
    if pd.isna(valor):
        return "N/A"
    # Formata com padrão americano primeiro, depois inverte separadores
    formatado = f"{valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    return f"{prefixo}{formatado}"

def formata_num(valor):
    # Formata apenas o número com vírgula decimal (ex: 9,86)
    return f"{valor:.2f}".replace(".", ",")

# Configuração da página e Identidade Visual (Cores Boticário)
st.set_page_config(page_title="Martech Analytics | Case Boticário", layout="wide")

# Estilo CSS para cores da marca e cartões de métricas
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    h1, h2, h3 { color: #004731; font-family: 'Arial'; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); border-left: 5px solid #004731; }
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
# CABEÇALHO & KPIs
# ---------------------------------------------------------
st.title("📊 Análise de Performance: Campanhas de Inverno")
st.markdown("---")

col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
inv_total = df['Investimento_Mkt'].sum()
rec_total = df['Receita_Gerada'].sum()
roas_total = rec_total / inv_total

# Aplicando a formatação brasileira nos KPIs
col_kpi1.metric("Investimento Total", formata_br(inv_total))
col_kpi2.metric("Receita Gerada", formata_br(rec_total))
col_kpi3.metric("ROAS Geral", f"{formata_num(roas_total)}x")
col_kpi4.metric("Meta", "Perfumaria", delta_color="normal")

# ---------------------------------------------------------
# BLOCO 1: VISÃO GERAL DE CANAIS
# ---------------------------------------------------------
st.header("1. Eficiência Real por Canal")
col_graf1, col_text1 = st.columns([2, 1])

with col_graf1:
    fig_combo = go.Figure()
    
    # Barras de Investimento
    fig_combo.add_trace(go.Bar(
        x=df_canal['Canal'], 
        y=df_canal['Investimento_Mkt'], 
        name='Investimento (R$)', 
        marker_color='#E2E2E2'
    ))
    
    # Linha de ROAS
    fig_combo.add_trace(go.Scatter(
        x=df_canal['Canal'], 
        y=df_canal['ROAS'], 
        name='ROAS', 
        yaxis='y2', 
        line=dict(color='#D4AF37', width=4),
        marker=dict(size=10)
    ))
    
    fig_combo.update_layout(
        title="Volume de Investimento vs. Retorno (ROAS)",
        yaxis=dict(title="Investimento (R$)"),
        yaxis2=dict(title="ROAS", overlaying='y', side='right'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="simple_white",
        # ESSENCIAL: Configura o Plotly para usar vírgula decimal e ponto de milhar
        separators=',.'
    )
    st.plotly_chart(fig_combo, use_container_width=True)

with col_text1:
    st.info(f"""
    **Principais Insights:**
    - O **Google Search** é o grande motor de rentabilidade da conta.
    - A **Mídia Programática** apresenta o menor ROAS ({formata_num(0.25)}), indicando que o tráfego de baixo custo não está convertendo em vendas diretas.
    - Canais com intenção de busca superam canais de alcance em conversão.
    """)

# ---------------------------------------------------------
# BLOCO 2: DEEP DIVE CATEGORIAS (O CORAÇÃO DO CASE)
# ---------------------------------------------------------
st.header("2. O Desafio da Perfumaria e Influenciadores")
col_graf2, col_graf3 = st.columns(2)

with col_graf2:
    df_perf = df[df['Categoria_Anunciada'] == 'Perfumaria'].groupby('Canal').agg({
        'Investimento_Mkt': 'sum', 
        'Receita_Gerada': 'sum'
    }).reset_index()
    df_perf['ROAS'] = df_perf['Receita_Gerada'] / df_perf['Investimento_Mkt']
    
    fig_perf = px.bar(
        df_perf, x='Canal', y='ROAS', 
        title="ROAS em Perfumaria (Meta do Trimestre)",
        color_discrete_sequence=['#004731'], 
        text_auto='.2f'
    )
    fig_perf.update_layout(separators=',.')
    st.plotly_chart(fig_perf, use_container_width=True)
    st.warning(f"Ponto de Atenção: Influenciadores em Perfumaria operam abaixo do break-even (ROAS {formata_num(0.84)}).")

with col_graf3:
    df_influ = df[df['Canal'] == 'Influenciadores'].groupby('Categoria_Anunciada').agg({
        'Investimento_Mkt': 'sum', 
        'Receita_Gerada': 'sum'
    }).reset_index()
    df_influ['ROAS'] = df_influ['Receita_Gerada'] / df_influ['Investimento_Mkt']
    
    fig_influ = px.bar(
        df_influ, x='Categoria_Anunciada', y='ROAS', 
        title="Performance de Influenciadores por Categoria",
        color_discrete_sequence=['#D4AF37'], 
        text_auto='.2f'
    )
    fig_influ.update_layout(separators=',.')
    st.plotly_chart(fig_influ, use_container_width=True)
    st.success("Insight: O canal de Influenciadores brilha na categoria Maquiagem.")

# ---------------------------------------------------------
# BLOCO 3: CONCLUSÃO E RECOMENDAÇÃO
# ---------------------------------------------------------
st.markdown("---")
st.header("3. Recomendação de Alocação: R$ 50.000 Extra")

rec_col1, rec_col2, rec_col3 = st.columns(3)

with rec_col1:
    st.success("🚀 **Prioridade 1: Google Search**")
    st.write(f"Alocação sugerida: **{formata_br(35000)}**")
    st.write(f"Foco: Termos de fundo de funil para Perfumaria (ROAS {formata_num(9.86)}x).")

with rec_col2:
    st.warning("📸 **Prioridade 2: Influenciadores**")
    st.write(f"Alocação sugerida: **{formata_br(10000)}**")
    st.write(f"Foco: Escalar Maquiagem e manter o branding em Perfumaria.")

with rec_col3:
    st.error("📉 **Prioridade 3: Programática**")
    st.write(f"Alocação sugerida: **{formata_br(5000)}**")
    st.write("Foco: Apenas Remarketing dinâmico para recuperação de carrinho.")

st.balloons()
