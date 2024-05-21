import streamlit as st
from model import Carteira

# Formulário de transações
st.title("Formulário de Transações")

# Janela de popup para adicionar transação
carteira = Carteira()
with st.form("Adicionar Transação"):
    criptomoeda = st.text_input('Criptomoeda')
    data = st.date_input('Data')
    valor = st.number_input('Valor')
    quantidade = st.number_input('Quantidade')
    tipo = st.selectbox('Tipo', ['compra', 'venda'])
    submit_button = st.form_submit_button(label='Adicionar Transação')
    if submit_button:
        carteira.adicionar_transacao(criptomoeda, data, valor, quantidade, tipo)

# Listar transações
st.title("Lista de Transações")
for transacao in carteira.transacoes:
    st.write(transacao)

# Calcular e exibir rendimento
rendimento = carteira.calcular_rendimento()
st.write(f'Rendimento: {rendimento}')