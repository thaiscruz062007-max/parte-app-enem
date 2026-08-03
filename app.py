import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ---------------------------------------------------------------------------------------#
# Configuração da página do Streamlit
# ---------------------------------------------------------------------------------------#
st.set_page_config(
    page_title="Dashboard ENEM - Análise Socioeconômica",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Análise do Desempenho no ENEM")
st.markdown("Explore os dados de desempenho médio no ENEM com base na localização geográfica, densidade populacional e estrutura docente.")

# ---------------------------------------------------------------------------------------#
# Funções de Suporte e Processamento
# ---------------------------------------------------------------------------------------#

@st.cache_data
def load_data():
    # Altere o caminho do arquivo conforme a localização no seu repositório do GitHub
    # Exemplo: 'df_2014-2019.csv' ou 'data/df_2014-2019.csv'
    data = pd.read_csv('df_2014-2019.csv')
    st.subheader("Visualização dos Dados")
    
    
    # Seleção de colunas via iloc para evitar problemas com UTF-8
    medias_uf = data.iloc[:, [0, 1, 59]].copy()
    media_espaco = data.iloc[:, [0, 70, 69, 59]].copy()
    media_docentes = data.iloc[:, [0, 73, 59]].copy()

    # Renomeando as colunas
    medias_uf.columns = ['ANO', 'SIGLA_UF', 'MEDIA_NOTAS']
    media_espaco.columns = ['ANO', 'ESCOLA_KM2', 'HABITANTES_KM2', 'MEDIA_NOTAS']
    media_docentes.columns = ['ANO', 'DOCENTES_ESCOLA', 'MEDIA_NOTAS']

    return medias_uf, media_espaco, media_docentes

def associateUf(df: pd.DataFrame):
    return df.groupby(['SIGLA_UF', 'ANO'])['MEDIA_NOTAS'].mean().reset_index()

# ---------------------------------------------------------------------------------------#
# Carregamento dos Dados
# ---------------------------------------------------------------------------------------#
try:
    medias_uf, media_espaco, media_docentes = load_data()
    medias_uf_grouped = associateUf(medias_uf)
    st.subheader("Visualização dos Dados")
    st.dataframe(medias_uf.head(25))

    # ---------------------------------------------------------------------------------------#
    # Seção 1: Desempenho Médio por UF (Gráfico Interativo)
    # ---------------------------------------------------------------------------------------#
    st.header("1. Desempenho Médio no ENEM por Estado (UF)")
    
    # Filtro Interativo de UF
    lista_ufs = sorted(medias_uf_grouped['SIGLA_UF'].unique())
    uf_selecionada = st.selectbox("Selecione o Estado (UF):", lista_ufs, index=lista_ufs.index('BA') if 'BA' in lista_ufs else 0)

    # Plotagem do Gráfico da UF selecionada
    df_uf = medias_uf_grouped[medias_uf_grouped["SIGLA_UF"] == uf_selecionada]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df_uf["ANO"], df_uf["MEDIA_NOTAS"], marker='o', color='#1f77b4', linewidth=2)
    ax.set_ylim(0, 1000)
    ax.set_title(f'{uf_selecionada}: Desempenho médio no ENEM')
    ax.set_xlabel("Ano")
    ax.set_ylabel("Média de Notas")
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.grid(True, linestyle='--', alpha=0.6)

    # Exibe o gráfico no Streamlit
    st.pyplot(fig)

    st.divider()

    # ---------------------------------------------------------------------------------------#
    # Seção 2: Fatores Geográficos e Populacionais
    # ---------------------------------------------------------------------------------------#
    st.header("2. Relação com Indicadores Geográficos e Populacionais")
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Escolas por km² vs Média")
        fig_area, ax_area = plt.subplots(figsize=(6, 4))
        ax_area.scatter(media_espaco["ESCOLA_KM2"], media_espaco["MEDIA_NOTAS"], alpha=0.5, color='green')
        ax_area.set_xlabel("Escolas por km²")
        ax_area.set_ylabel("Média do ENEM")
        ax_area.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig_area)

    with col2:
        st.subheader("Habitantes por km² vs Média")
        fig_hab, ax_hab = plt.subplots(figsize=(6, 4))
        ax_hab.scatter(media_espaco["HABITANTES_KM2"], media_espaco["MEDIA_NOTAS"], alpha=0.5, color='orange')
        ax_hab.set_xlabel("Habitantes por km²")
        ax_hab.set_ylabel("Média do ENEM")
        ax_hab.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig_hab)

    st.divider()

    # ---------------------------------------------------------------------------------------#
    # Seção 3: Relação com Infraestrutura Docente
    # ---------------------------------------------------------------------------------------#
    st.header("3. Relação com Número de Docentes por Escola")

    fig_doc, ax_doc = plt.subplots(figsize=(8, 4))
    ax_doc.scatter(media_docentes["DOCENTES_ESCOLA"], media_docentes["MEDIA_NOTAS"], alpha=0.5, color='purple')
    ax_doc.set_xlabel("Média de Docentes por Escola")
    ax_doc.set_ylabel("Média do ENEM")
    ax_doc.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig_doc)

except FileNotFoundError:
    st.error("Arquivo 'df_2014-2019.csv' não encontrado. Certifique-se de que o arquivo esteja na mesma pasta do código no GitHub.")
