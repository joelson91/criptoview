import streamlit as st
from model import Tabela

tabela = Tabela("bitcoin", "usd", "7")
st.dataframe(tabela.dataframe)