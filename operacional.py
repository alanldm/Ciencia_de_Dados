import pandas as pd
import geopandas as gpd
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st

def funcao(dados):
    funcao = dados.loc[:,["registration_aviation","type_operation"]]

    #Removendo dados inconclusivos: UNKNOWN.
    funcao = funcao[(funcao.registration_aviation!="UNKNOWN") & (funcao.type_operation!="UNKNOWN")]

    #Criando uma coluna de booleanos, onde o valor True representa as aeronaves que se acidentaram operando na função para qual foram registradas.
    funcao["function"] = funcao.registration_aviation == funcao.type_operation

    #Criando um vetor para armazenar os valores verdadeiros e falsos.
    qtd = [funcao.function[funcao.function==True].count(), funcao.function[funcao.function==False].count()]
    
    fig = px.pie(values=qtd, names=["Iguais", "Diferentes"], title="Comparação entre os tipos de registro e de operação")
    st.plotly_chart(fig)

def estagio(dados):
    #Gerando um dataframe com as colunas de fase de operação ('operation_phase') e de identificador do acidente ('occurrence_id').
    fase = dados.loc[:,["occurrence_id", "operation_phase"]]

    #Removendo os valores faltantes e inconclusivos.
    fase.dropna(inplace=True)
    fase = fase[fase.operation_phase!="UNKNOWN"]

    #Agrupando os dados com base no momento do acidente.
    fase = fase.groupby("operation_phase").count()
    fase.reset_index(inplace=True) #Reorganizando os índices.

    #Renomeando as colunas do dataframe.
    fase.rename(columns={"operation_phase":"Fase", "occurrence_id":"Quantidades"}, inplace=True)
    fase = fase[fase.Quantidades>100] #Filtrando para manter apenas os Top 5 momentos com mais acidentes.
    fase.sort_values(by="Quantidades", inplace=True, ascending=True) #Ordenando os dados.

    fig = px.bar(fase, x="Fase", y="Quantidades")
    st.plotly_chart(fig)

def mostra_graficos_operacional(dados):
    funcao(dados)
    estagio(dados)

