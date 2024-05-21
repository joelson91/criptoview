import streamlit as st
import coingecko
import pandas as pd

# Gerenciar segredos do Coingecko
st.set_page_config(layout="wide")
coingecko_key = st.secrets["coingecko_key"]

# Classe Tabela para encapsular lógica de recuperação de dados
class Tabela:
    def __init__(self, id, moeda, dias):
        self.id = id
        self.moeda = moeda
        self.dias = dias
        self.dataframe = self.get_dataframe()

    def get_dataframe(self):
        # Conectar à API Coingecko
        cg = coingecko.CoinGeckoDemoClient(api_key=coingecko_key)

        # Recuperar dados de preços
        response = cg.coins.get_market_chart(self.id, self.moeda, self.dias)
        prices = response['prices']

        # Converter dados em DataFrame
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
        df = df[['date', 'price']]
        return df

# Implementação da carteira
class Carteira:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, criptomoeda, data, valor, tipo):
        transacao = {
            'criptomoeda': criptomoeda,
            'data': data,
            'valor': valor,
            'tipo': tipo
        }
        self.transacoes.append(transacao)

    def calcular_rendimento(self):
        rendimento = 0
        for transacao in self.transacoes:
            if transacao['tipo'] == 'compra':
                rendimento -= transacao['valor']
            elif transacao['tipo'] == 'venda':
                rendimento += transacao['valor']
        return rendimento