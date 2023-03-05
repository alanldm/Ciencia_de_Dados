import pandas as pd
import geopandas as gpd
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st
st.set_page_config(layout="wide")
import tratamento
import espacial
import temporal
import aeronaves
import operacional
import empresas

dados, Estados = tratamento.tratamento()

st.sidebar.image("ufrn-logo-5-599x192.png")
escolha = st.sidebar.selectbox("Escolha uma categoria: ", ["Aeronaves", "Temporal", "Espacial", "Operacional", "Empresas"])
st.sidebar.text('''Grupo:
Alan Lima de Medeiros
''')
#st.write(dados)

if escolha == "Espacial":
    st.title("Informações geográficas")
    espacial.mostra_graficos_espaciais(dados, Estados)
elif escolha == "Temporal":
    st.title("Informações temporais")
    temporal.mostra_graficos_temporais(dados)
elif escolha == "Aeronaves":
    st.title("Informações sobre as aeronaves")
    aeronaves.mostra_graficos_aeronaves(dados)
elif escolha == "Operacional":
    st.title("Informações operacionais")
    operacional.mostra_graficos_operacional(dados)
elif escolha == "Empresas":
    st.title("Informações sobre as empresas")
    empresas.mostra_graficos_empresas(dados)
