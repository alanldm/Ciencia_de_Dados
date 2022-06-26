import pandas as pd
import geopandas as gpd
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st
import tratamento
import espacial
import temporal
import aeronaves
import operacional
import empresas

dados, Estados = tratamento.tratamento()

st.sidebar.image("ufrn-logo-5-599x192.png")
escolha = st.sidebar.selectbox("Escolha uma categoria: ", ["Temporal", "Espacial", "Aeronaves", "Operacional", "Empresas"])
#st.write(dados)

if escolha == "Espacial":
    espacial.mostra_graficos_espaciais(dados, Estados)
elif escolha == "Temporal":
    temporal.mostra_graficos_temporais(dados)
elif escolha == "Aeronaves":
    aeronaves.mostra_graficos_aeronaves(dados)
elif escolha == "Operacional":
    operacional.mostra_graficos_operacional(dados)
elif escolha == "Empresas":
    empresas.mostra_graficos_empresas(dados)
