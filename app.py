import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Configuração da Página
st.set_page_config(page_title="Martech Analytics | Case Boticário", layout="wide")

# Configuração de Estilo e Cores (Paleta O Boticário)
boticario_green = "#004731"
boticario_gold = "#D4AF37"
neutral_gray = "#F2F2F2"
text_color = "#575756"

sns.set_theme(style="white")

# 2. Carregamento e Processamento de Dados
@st.cache_data
def load_data():
    df = pd.read_csv('Case_Midia_Produto.csv')
    return df

df = load_data()

# Cálculos Consolidados
df_canal = df.groupby('Canal').agg({
    'Investimento_Mkt': 'sum', 
    'Receita_Gerada': 'sum'
}).reset_index()
df_canal['ROAS'] = df_canal['Receita_Gerada'] / df_canal['Investimento_Mkt']
df_canal = df_canal.sort_values('ROAS', ascending=False)

# ---------------------------------------------------------
# HEADER & KPIs
# ---------------------------------------------------------
st.title("📊 Dashboard de Performance: Campanhas de Inverno")
st.markdown(f"<p style='color:{text_color};'>Análise estratégica de Mídia e Performance para meta de Perfumaria.</p>", unsafe_allow_html=True)
st.markdown("---")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
inv_total = df['Investimento_Mkt'].sum()
rec_total = df['Receita_Gerada'].sum()
roas_total = rec_total / inv_total

kpi1.metric("Investimento Total", f"R$ {inv_total:,.2f}")
kpi2.metric("Receita Gerada", f"R$ {rec_total:,.2f}")
kpi3.metric("ROAS Médio", f"{roas_total:.2f}x")
kpi4.metric("Status Meta", "Foco Perfumaria")

# ---------------------------------------------------------
# BLOCO 1: VISÃO GERAL (COMBO CHART SEABORN)
# ---------------------------------------------------------
st.header("1. Investimento vs. Eficiência por Canal")
fig1, ax1 = plt.subplots(figsize=(12, 6))

# Barras de Investimento
sns.barplot(data=df_canal, x='Canal', y='Investimento_Mkt', color='#E2E2E2', ax=ax1)
ax1.set_ylabel('Investimento (R$)', fontweight='bold', color=text_color)
ax1.set_xlabel('')

# Eixo Duplo para ROAS
ax2 = ax1.twinx()
sns.lineplot(data=df_canal, x='Canal', y='ROAS', marker='o', color=boticario_gold, linewidth=3, markersize=10, ax=ax2)
ax2.set_ylabel('ROAS (Eficiência)', fontweight='bold', color=boticario_gold)

# Labels na linha de ROAS
for i, val in enumerate(df_canal['ROAS']):
    ax2.text(i, val + 0.3, f'{val:.2f}x', color=boticario_green, fontweight='bold', ha='center')

sns.despine(top=True, right=False, left=False)
st.pyplot(fig1)

# ---------------------------------------------------------
# BLOCO 2: DEEP DIVE (PERFUMARIA E INFLUENCIADORES)
# ---------------------------------------------------------
st.header("2. O Desafio da Perfumaria")
col_a, col_b = st.columns(2)

with col_a:
    # ROAS Perfumaria por Canal
    df_perf = df[df['Categoria_Anunciada'] == 'Perfumaria'].groupby('Canal').agg({
        'Investimento_Mkt': 'sum', 'Receita_Gerada': 'sum'
    }).reset_index()
    df_perf['ROAS'] = df_perf['Receita_Gerada'] / df_perf['Investimento_Mkt']
    df_perf = df_perf.sort_values('ROAS', ascending=False)

    fig2, ax_perf = plt.subplots(figsize=(8, 6))
    colors = [boticario_gold if (x == df_perf['ROAS'].max()) else boticario_green for x in df_perf['ROAS']]
    sns.barplot(data=df_perf, x='Canal', y='ROAS', palette=colors, ax=ax_perf)
    
    # Data Labels
    for p in ax_perf.patches:
        ax_perf.annotate(f'{p.get_height():.2f}x', (p.get_x() + p.get_width()/2., p.get_height()),
                         ha='center', va='bottom', fontweight='bold', xytext=(0, 5), textcoords='offset points')
    
    ax_perf.set_title("ROAS na Categoria Perfumaria", fontweight='bold', color=boticario_green)
    ax_perf.axhline(1.0, color='red', linestyle='--', alpha=0.5) # Break-even
    sns.despine()
    st.pyplot(fig2)
    st.caption("Nota: Influenciadores e Programática performam abaixo de 1.0x em Perfumaria.")

with col_b:
    # ROAS Influenciadores por Categoria
    df_influ = df[df['Canal'] == 'Influenciadores'].groupby('Categoria_Anunciada').agg({
        'Investimento_Mkt': 'sum', 'Receita_Gerada': 'sum'
    }).reset_index()
    df_influ['ROAS'] = df_influ['Receita_Gerada'] / df_influ['Investimento_Mkt']
    
    fig3, ax_influ = plt.subplots(figsize=(8, 6))
    sns.barplot(data=df_influ, x='Categoria_Anunciada', y='ROAS', color=boticario_gold, ax=ax_influ)
    
    # Data Labels
    for p in ax_influ.patches:
        ax_influ.annotate(f'{p.get_height():.2f}x', (p.get_x() + p.get_width()/2., p.get_height()),
                         ha='center', va='bottom', fontweight='bold', xytext=(0, 5), textcoords='offset points')
        
    ax_influ.set_title("Eficiência de Influenciadores por Categoria", fontweight='bold', color=boticario_green)
    sns.despine()
    st.pyplot(fig3)
    st.caption("Insight: Influenciadores são motores de venda para Maquiagem.")

# ---------------------------------------------------------
# BLOCO 3: RECOMENDAÇÃO FINAL
# ---------------------------------------------------------
st.markdown("---")
st.header("3. Recomendação de Alocação (R$ 50.000 Extra)")

# Tabela Simples de Decisão
st.table(pd.DataFrame({
    'Canal': ['Google Search', 'Influenciadores', 'Mídia Programática'],
    'Verba Sugerida': ['R$ 35.000 (70%)', 'R$ 10.000 (20%)', 'R$ 5.000 (10%)'],
    'Racional': [
        'Maximizar ROAS de 9.8x em Perfumaria.',
        'Manter presença em Maquiagem (ROAS 3.9x).',
        'Reduzir apenas para Remarketing (Baixa conversão).'
    ]
}))

st.success("🎯 Foco em canais de intenção (Search) garante o atingimento da meta de Perfumaria.")

