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
    tabela = Tabela("bitcoin", "usd", "7")
    st.dataframe(tabela.dataframe)