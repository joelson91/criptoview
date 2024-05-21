import streamlit as st
from model import Tabela

# Título do aplicativo
st.title("Visualizador de Preços de Criptomoedas")

# Opções de seleção
moedas = ["usd", "eur", "brl"]
criptomoedas = ["bitcoin", "ethereum", "cardano", "solana", "polkadot"]

# Widgets de seleção
criptomoeda = st.selectbox("Selecione uma criptomoeda", criptomoedas, index=0, key="criptomoeda", help="Selecione a criptomoeda que deseja visualizar")
moeda_selecionada = st.selectbox("Selecione uma moeda", moedas, index=2, key="moeda", help="Selecione a moeda que deseja visualizar")
dias_selection = st.slider("Selecione o número de dias", 1, 365, 7)

# Criação da tabela
tabela = Tabela(criptomoeda , moeda_selecionada, dias_selection)

# Gráfico de preços
if criptomoeda is not None:
    st.title(f"Gráfico de Preços do {criptomoeda.capitalize()}")
    st.line_chart(tabela.dataframe.set_index('date'))