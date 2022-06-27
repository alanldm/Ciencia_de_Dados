import pandas as pd
import geopandas as gpd
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st

def periodo(dados):
    #Gerando dataframe com os dados de tempo ('time') e os identificadores de acidentes ('occurrence_id').
    periodo = dados.loc[:,["time", "occurrence_id"]]

    #Tratando os dados.
    periodo["Hora"] = periodo["time"].str.slice(start=0, stop=2) #Pegando apenas a hora da string.
    periodo["Hora"] = periodo["Hora"].astype(int) #Mudando do tipo string para inteiro.
    periodo.Hora[(periodo.Hora>=5) & (periodo.Hora<=18)] = "Dia" #Indicando quais horários representam o dia.
    periodo.Hora[periodo.Hora!="Dia"] = "Noite"  #Indicando quais horários representam a noite.
    periodo = periodo.groupby("Hora").count() #Agrupando os dados com base na hora.
    periodo.reset_index(inplace=True) #Reorganizando os índices.  
    periodo.rename(columns={"Hora":"Período", "time":"Quantidade"}, inplace=True) #Mudando o nome das colunas.

    fig = px.pie(periodo, values="Quantidade", names="Período", title="Quantidade de acidentes por período do dia", color="Período", color_discrete_map={'Dia':'yellow', "Noite":"Black"})
    st.plotly_chart(fig)

def anos(dados):
    #Calculando a idade das aeronaves:
    idade = dados.loc[:,["year_manufacture","occurrence_day"]] #Criando um dataframe apenas com as colunas do ano de fabricação e a data do acidente.
    idade.dropna(inplace=True) #Removendo os dados faltantes.

    #Extraindo as informações das strings da coluna dos dias dos acidentes.
    idade['occurrence_year'] = idade['occurrence_day'].str.slice(start=0,stop=4)
    idade['occurrence_month'] = idade['occurrence_day'].str.slice(start=5, stop=7)
    idade['year_manufacture'] = idade['year_manufacture'].astype(float) #Transformando os dados de strings para floats.
    idade['occurrence_year'] = idade['occurrence_year'].astype(float) #Transformando os dados de strings para floats.
    idade['age'] = idade['occurrence_year'] - idade['year_manufacture'] #Calculando a idade das aeronaves.
    idade = idade[idade.year_manufacture!=0] 
    anos_acidente = idade.groupby("occurrence_year").count() #Criando um dataframe a partir dos dados agrupados dos anos.
    anos_acidente.reset_index(inplace=True) #Reorganizando os índices.
    anos_acidente.drop(columns=["year_manufacture", "occurrence_day", "occurrence_month"], inplace=True) #Deixando apenas a coluna dos anos.
    anos_acidente.rename(columns={"occurrence_year":"Ano", "age":"Quantidade"}, inplace=True) #Renomeando as colunas.

    fig = px.bar(anos_acidente, x="Ano", y="Quantidade", title="Anos com mais acidentes", color="Quantidade", color_continuous_scale="Reds")
    st.plotly_chart(fig)

def idade(dados):
    idade = dados.loc[:,["year_manufacture","occurrence_day"]] #Criando um dataframe apenas com as colunas do ano de fabricação e a data do acidente.
    idade.dropna(inplace=True) #Removendo os dados faltantes.

    #Extraindo as informações das strings da coluna dos dias dos acidentes.
    idade['occurrence_year'] = idade['occurrence_day'].str.slice(start=0,stop=4)
    idade['occurrence_month'] = idade['occurrence_day'].str.slice(start=5, stop=7)
    idade['year_manufacture'] = idade['year_manufacture'].astype(float) #Transformando os dados de strings para floats.
    idade['occurrence_year'] = idade['occurrence_year'].astype(float) #Transformando os dados de strings para floats.
    idade['age'] = idade['occurrence_year'] - idade['year_manufacture'] #Calculando a idade das aeronaves.
    idade = idade[idade.year_manufacture!=0]
    idade = idade[idade.age>=0]
    idade.rename(columns={"age":"Idade"}, inplace=True)
    fig = px.histogram(idade, x="Idade", nbins=10, title="Idades das aeronaves acidentadas", opacity=0.4, color_discrete_sequence=['green'], log_y=True)
    st.plotly_chart(fig)

    idade = idade.sort_values(by="occurrence_month")

    idade.rename(columns={"occurrence_month":"Mês"}, inplace=True)
    fig = px.histogram(idade, x="Mês", nbins=10, color_discrete_sequence=['darkcyan'], title="Meses com mais acidentes")
    st.plotly_chart(fig)

def mostra_graficos_temporais(dados):
    col1, col2 = st.columns(2)

    with col1:
        periodo(dados)
        anos(dados)

    with col2:
        idade(dados)
