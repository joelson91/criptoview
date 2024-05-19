import pandas as pd
import requests
import streamlit as st

class Tabela:
    url_base = "https://api.coingecko.com/api/v3"

    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": st.secrets["coingecko_key"]
    }

    def __init__(self, id, moeda, dias):
        self.url = self.url_base + f"/coins/{id}/market_chart?vs_currency={moeda}&days={dias}&interval=daily"
        self.dataframe = self.get_dataframe()

    def get_response(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            return response.json()

    def create_dataframe(self, response):
        df = pd.DataFrame(response['prices'], columns=['timestamp', 'price'])
        df['market_cap'] = pd.DataFrame(response['market_caps'], columns=['timestamp', 'market_cap'])['market_cap']
        df['total_volume'] = pd.DataFrame(response['total_volumes'], columns=['timestamp', 'total_volume'])['total_volume']
        return df

    def convert_timestamp(self, df):
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    
    def delete_columns(self, df):
        df = df.drop(['timestamp', 'total_volume', 'market_cap'], axis=1)
        return df

    def reorder_columns(self, df):
        df = df[['date', 'price']]
        return df

    def get_dataframe(self):
        response = self.get_response()
        df = self.create_dataframe(response)
        df = self.convert_timestamp(df)
        df = self.delete_columns(df)
        df = self.reorder_columns(df)
        return df

if __name__ == "__main__":

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