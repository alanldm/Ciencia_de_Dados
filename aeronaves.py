import pandas as pd
import geopandas as gpd
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st

def models(dados):
    #Gerando um dataframe de modelos a partir das colunas de modelos ('model') e de ids ('occurrence_id').
    modelos = dados[["occurrence_id", "model"]]
    modelos = modelos[modelos.model!="***"] #Filtrando os dados inconsistentes.
    modelos = modelos.groupby("model").count() #Agrupando os valores a partir da coluna de modelos.
    modelos.reset_index(inplace=True) #Reorganizando os índices.
    modelos.rename(columns={"model":"Modelos", "occurrence_id":"Quantidades"}, inplace=True) #Trocando o nome das colunas.
    modelos = modelos[modelos.Quantidades>=30] #Filtrando os dados para pegar apenas os 11 com mais acidentes.
    modelos.sort_values(by="Quantidades", inplace=True, ascending=True) #Ordenando os dados.

    fig = px.bar(modelos, x="Modelos", y="Quantidades")
    st.plotly_chart(fig)

def motors(dados):
    motores = dados.loc[:,["occurrence_id", "engines_amount"]] #Pegando apenas as colunas de id e de número de motores.
    motores.dropna(inplace=True) #Removendo as linhas nulas.
    motores = motores.groupby("engines_amount").count() #Contando o número de acidentes pela quantidade de motores.
    motores.reset_index(inplace=True) #Reorganizando os índices.
    motores.rename(columns={"engines_amount":"Motores", "occurrence_id":"Quantidades"}, inplace=True) #Trocando o nome das colunas.
    motores.sort_values(by="Quantidades", inplace=True, ascending=True) #Ordenando os dados.

    fig = px.bar(motores, x="Motores", y="Quantidades")
    st.plotly_chart(fig)

def types(dados):
    #Gerando um dataframe com os tipos de aeronaves ('equipment') e os identificadores dos acidentes ('occurrence_id'). 
    tipos = dados[["occurrence_id","equipment"]]
    tipos = tipos[tipos.equipment!='UNKNOWN']

    #Agrupando os dados com base no tipo de aeronave.
    x = tipos.groupby("equipment").count()

    x.reset_index(inplace=True) #Reorganizando os índices.
    x = x.append({"equipment":"Outros", "occurrence_id":19}, ignore_index=True)
    x = x[x.occurrence_id>=19]

    fig = px.pie(x, values="occurrence_id", names=["Avião", "Helicóptero", "Ultraleve", "Outros"], title="Tipos de aeronaves acidentadas")
    st.plotly_chart(fig)

def damage(dados):
    #Montando o dataframe com a coluna de ids ('occurrence_id') e de danos ('damage_level').
    dano = dados.loc[:,["occurrence_id", "damage_level"]]
    dano = dano[dano.damage_level!="UNKNOWN"] #Removendo dados inconsistentes.
    dano = dano.groupby("damage_level").count() #Agrupando os dados com base no nível do dano.
    dano.reset_index(inplace=True) #Reorganizando os índices do dataframe.
    dano.rename(columns={"damage_level":"Danos", "occurrence_id":"Quantidades"}, inplace=True) #Renomeando as colunas do dataframe.

    fig = px.pie(dano, values="Quantidades", names=["Destruído", "Leve", "Nenhum", "Substancial"], title="Gráfico de setores dos tipos de danos")
    st.plotly_chart(fig)

def mostra_graficos_aeronaves(dados):
    types(dados)
    damage(dados)
    models(dados)
    motors(dados)