import pandas as pd
import geopandas as gpd
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st

def empresa(dados):
    #Gerando um dataframe com as colunas de empresas ('manufacturer') e o identificador de acidentes ('occurrence_id').
    empresas = dados.loc[:,["manufacturer", "occurrence_id"]]
    empresas = empresas[empresas.manufacturer!="***"] #Removendo os valores inválidos.

    #Agrupando os dados a partir da coluna das empresas.
    top10 = empresas.groupby("manufacturer").count()
    top10 = top10[top10.occurrence_id>=34] #Filtrando para ficar apenas com as 10 empresas com mais acidentes.
    top10.reset_index(inplace=True) #Reorganizando os índices.
    top10.rename(columns={"manufacturer":"Empresas","occurrence_id":"Quantidades"}, inplace=True) #Renomeando as colunas.
    top10.sort_values(by="Quantidades", inplace=True, ascending=False) #Ordenando as empresas.

    fig = px.bar(top10, x=["Neiva", "Cessna", "Piper", "Embraer", "Aero", "Beech", "Robinson", "Bell", "Helibras", "Boeing"], y="Quantidades")
    st.plotly_chart(fig)

def mostra_graficos_empresas(dados):
    empresa(dados)