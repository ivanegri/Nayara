import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Dashboard de Clientes", layout="wide")

st.title("Dashboard de Clientes")

# O decorador @st.cache_data é usado corretamente na função para otimizar o carregamento dos dados.
@st.cache_data
def load_data():
    df = pd.read_csv('clientes_data.csv')
    df['Data_Ativação'] = pd.to_datetime(df['Data_Ativação'])
    df['Data_Cancelamento'] = pd.to_datetime(df['Data_Cancelamento'])
    return df

# Carregamos os dados e os atribuímos a uma variável.
df = load_data()

# --- FILTROS NA BARRA LATERAL ---
st.sidebar.header("Filtros")

# O valor selecionado no selectbox é armazenado em uma variável.
# A lista de consultores é gerada dinamicamente a partir do DataFrame.
consultor_selecionado = st.sidebar.selectbox(
    "Selecione o Consultor",
    ["Todos"] + list(df['Consultor'].unique())
)

status_selecionado = st.sidebar.selectbox(
    "Selecione o Status",
    ["Todos", "Ativo", "Cancelado"]
)

# --- FILTRAGEM DO DATAFRAME ---
# Criamos uma cópia do DataFrame para aplicar os filtros.
df_filtrado = df.copy()
if consultor_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Consultor'] == consultor_selecionado]

if status_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Status'] == status_selecionado]


# --- EXIBIÇÃO DO GRÁFICO ---
# O gráfico agora usa o DataFrame filtrado.
fig = px.scatter(df_filtrado,
                 x="Data_Ativação",
                 y="CSAT",
                 color='Status',
                 color_discrete_map={'Ativo': 'green', 'Cancelado': 'red'},
                 symbol='Consultor',
                 title="Análise de CSAT por Data de Ativação",
                 hover_data=['Cliente'])

# Usamos st.plotly_chart para exibir o gráfico no Streamlit.
st.plotly_chart(fig, use_container_width=True)

# --- GRÁFICO DE TEMPO DE ATIVIDADE (CANCELADOS) ---
st.subheader("Análise de Tempo de Atividade dos Clientes Cancelados")

# Filtra apenas os clientes cancelados do dataframe já filtrado (respeitando o filtro de consultor)
df_cancelados = df_filtrado[df_filtrado['Status'] == 'Cancelado'].copy()

# Verifica se há dados de cancelamento para exibir
if not df_cancelados.empty:
    # Calcula o tempo de atividade em dias. Usamos .copy() para evitar SettingWithCopyWarning.
    df_cancelados['Tempo_Ativo_Dias'] = (df_cancelados['Data_Cancelamento'] - df_cancelados['Data_Ativação']).dt.days

    fig_tempo_ativo = px.bar(
        df_cancelados,
        x='Cliente',
        y='Tempo_Ativo_Dias',
        title='Tempo de Atividade Antes do Cancelamento (por Cliente)',
        labels={'Tempo_Ativo_Dias': 'Tempo Ativo (dias)', 'Cliente': 'Cliente'},
        color='Consultor',
        hover_data=['Motivo_Cancelamento']
    )
    st.plotly_chart(fig_tempo_ativo, use_container_width=True)
else:
    st.warning("Não há dados de clientes cancelados para os filtros selecionados.")

# --- GRÁFICO DE CSAT MÉDIO POR CONSULTOR ---
st.subheader("CSAT Médio por Consultor")

# Garante que não há valores nulos de CSAT para o cálculo da média
df_csat = df_filtrado.dropna(subset=['CSAT']).copy()

if not df_csat.empty:
    # Agrupa por Consultor e Status, calcula a média do CSAT e reseta o índice
    avg_csat_por_consultor = df_csat.groupby(['Consultor', 'Status'])['CSAT'].mean().reset_index()

    # Cria o gráfico de barras horizontais
    fig_csat_consultor = px.bar(
        avg_csat_por_consultor,
        y='Consultor',
        x='CSAT',
        color='Status',
        title='CSAT Médio por Consultor (Ativos vs. Cancelados)',
        labels={'CSAT': 'CSAT Médio (de 1 a 5)', 'Consultor': 'Consultor'},
        orientation='h',
        barmode='group',
        color_discrete_map={'Ativo': 'green', 'Cancelado': 'red'},
        text_auto='.2f'  # Exibe o valor da média na barra
    )
    st.plotly_chart(fig_csat_consultor, use_container_width=True)
else:
    st.warning("Não há dados de CSAT para os filtros selecionados.")

# Opcional: Exibir a tabela com os dados filtrados
st.subheader("Dados Filtrados")
st.dataframe(df_filtrado)