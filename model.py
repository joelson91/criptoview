import pandas as pd
import streamlit as st
import coingecko

class Tabela:
    cg = coingecko.CoinGeckoDemoClient(api_key=st.secrets["coingecko_key"])

    def __init__(self, id, moeda, dias):
        self.id = id
        self.moeda = moeda
        self.dias = dias
        self.dataframe = self.get_dataframe()

    def get_dataframe(self):
        response = self.cg.coins.get_market_chart(self.id, self.moeda, self.dias)
        prices = response['prices']
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
        df = df[['date', 'price']]
        return df

if __name__ == "__main__":
    st.title("Visualizador de Preços de Criptomoedas")

    moedas = ["usd", "eur", "brl"]
    criptomoedas = ["bitcoin", "ethereum", "cardano", "solana", "polkadot"]

    criptomoeda = st.selectbox("Selecione uma criptomoeda", criptomoedas, index=0, key="criptomoeda", help="Selecione a criptomoeda que deseja visualizar")
    moeda_selecionada = st.selectbox("Selecione uma moeda", moedas, index=2, key="moeda", help="Selecione a moeda que deseja visualizar")
    dias_selection = st.slider("Selecione o número de dias", 1, 365, 7)

    tabela = Tabela(criptomoeda , moeda_selecionada, dias_selection)

    if criptomoeda is not None:
        st.title(f"Gráfico de Preços do {criptomoeda.capitalize()}")
        st.line_chart(tabela.dataframe.set_index('date'))