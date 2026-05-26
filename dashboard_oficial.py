# -*- coding: utf-8 -*-
"""
Created on Fri May 15 15:50:29 2026

@author: amanda.costa
"""

# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt

# SINAL VERDE PARA O WINDOWS: Evita que o gráfico trave o carregamento do site!
import matplotlib
matplotlib.use('Agg')

# 1. Configuração de Layout do Dashboard Web
st.set_page_config(
    page_title="Dashboard Climático - Embrapa Pacajus",
    page_icon="📊",
    layout="wide"
)

# Estilização CSS para forçar um visual bonito e claro (Padrão Embrapa)
st.markdown("""
    <style>
    .header-box { background-color: #0b5345; padding: 20px; border-radius: 8px; color: white; margin-bottom: 25px; }
    .metric-card { background-color: #ffffff; border-left: 5px solid #117a65; padding: 15px; border-radius: 4px; box-shadow: 1px 1px 5px rgba(0,0,0,0.1); color: #2c3e50; }
    .metric-title { font-size: 14px; color: #7f8c8d; font-weight: bold; }
    .metric-value { font-size: 24px; color: #117a65; font-weight: bold; }
    h1, h2, h3, p { color: #2c3e50 !important; }
    </style>
""", unsafe_allow_html=True)

# 2. Barra Lateral (Coordenadas e Informações Técnicas)
st.sidebar.markdown("### 📍 Estação Experimental")
st.sidebar.info("""
**Unidade:** Pacajus - CE
**Latitude:** 4° 10' 21'' S
**Longitude:** 38° 27' 38'' O
**Altitude:** 70 m
""")

# Caminho da sua planilha local FUNCEME
caminho_local = r"C:\Users\amanda.costa\Documents\Dados FUNCEME\2026\20260515Precipitação.xlsx"
st.sidebar.markdown("---")
st.sidebar.markdown("**Fonte de Dados:**")
st.sidebar.caption(f"📁 `{caminho_local}`")

# 3. Função de Carga dos Dados
@st.cache_data
def carregar_dados(caminho):
    try:
        df_excel = pd.read_excel(caminho)
        df_excel.columns = ['Horario', 'Temperatura', 'Umidade', 'Vento']
        return df_excel, False
    except Exception as e:
        # Se não achar a planilha, gera dados para o painel não ficar em branco
        datas = pd.date_range(start="2026-05-15 00:00", periods=6, freq="4H")
        df_mock = pd.DataFrame({
            'Horario': datas.strftime('%H:%M'),
            'Temperatura': [23.5, 22.0, 26.8, 31.2, 29.5, 25.0],
            'Umidade': [82, 85, 68, 52, 58, 75],
            'Vento': [14.0, 11.5, 16.2, 24.0, 19.5, 15.0]
        })
        return df_mock, True

df, usando_simulacao = carregar_dados(caminho_local)

# 4. Painel Principal / Banner
st.markdown("""
    <div class="header-box">
        <h2 style='margin:0; font-size: 26px; color: white !important;'>Painel de Monitoramento Climatológico</h2>
        <p style='margin:5px 0 0 0; opacity:0.8; color: white !important;'>Embrapa Agroindústria Tropical — Campo Experimental de Pacajus</p>
    </div>
""", unsafe_allow_html=True)

if usando_simulacao:
    st.warning("⚠️ Exibindo dados de demonstração. Verifique se a planilha está salva em: " + caminho_local)

# 5. Blocos de Métricas (Última Leitura)
st.markdown("### ⚡ Condições Atuais")
ultimo_registro = df.iloc[-1]

m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>🌡️ TEMPERATURA</div><div class='metric-value'>{ultimo_registro['Temperatura']} °C</div></div>", unsafe_allow_html=True)
with m_col2:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>💧 UMIDADE</div><div class='metric-value'>{ultimo_registro['Umidade']} %</div></div>", unsafe_allow_html=True)
with m_col3:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>💨 VENTO</div><div class='metric-value'>{ultimo_registro['Vento']} km/h</div></div>", unsafe_allow_html=True)
with m_col4:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>⏰ HORÁRIO</div><div class='metric-value'>{ultimo_registro['Horario']}</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 6. Gráficos e Tabela de Dados Lado a Lado
st.markdown("### 📊 Histórico Diário")
col_grafico, col_tabela = st.columns([2, 1])

with col_grafico:
    fig, ax = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    fig.patch.set_facecolor('#ffffff')
    
    for a in ax:
        a.grid(True, linestyle=':', alpha=0.6, color='#bdc3c7')
        a.spines['top'].set_visible(False)
        a.spines['right'].set_visible(False)

    ax[0].plot(df['Horario'], df['Temperatura'], color='#d35400', marker='o', linewidth=2)
    ax[0].set_ylabel('Temp. (°C)', fontweight='bold')
    
    ax[1].plot(df['Horario'], df['Umidade'], color='#2980b9', marker='s', linewidth=2)
    ax[1].set_ylabel('Umid. (%)', fontweight='bold')
    
    ax[2].plot(df['Horario'], df['Vento'], color='#27ae60', marker='^', linewidth=2)
    ax[2].set_ylabel('Vento (km/h)', fontweight='bold')
    ax[2].set_xlabel('Horário dos Registros')
    
    plt.tight_layout()
    st.pyplot(fig)

with col_tabela:
    st.markdown("##### 📋 Dados Analisados")
    st.dataframe(df, hide_index=True, use_container_width=True)