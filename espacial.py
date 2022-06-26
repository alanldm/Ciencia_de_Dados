import pandas as pd
import geopandas as gpd
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_folium import folium_static

def grafico_regiao(dados, Estados):
    tipo_op = dados.loc[:, ['type_operation', 'fu']]

    tipo_op = tipo_op[tipo_op.type_operation != 'UNKNOWN']

    sudeste = tipo_op[(tipo_op.fu == 'SP')|(tipo_op.fu == 'RJ')|(tipo_op.fu == 'ES')|(tipo_op.fu == 'MG')]
    sul = tipo_op[(tipo_op.fu == 'RS')|(tipo_op.fu == 'SC')|(tipo_op.fu == 'PR')]
    centro = tipo_op[(tipo_op.fu == 'DF')|(tipo_op.fu == 'GO')|(tipo_op.fu == 'MT')|(tipo_op.fu == 'MS')]
    norte = tipo_op[(tipo_op.fu == 'AM')|(tipo_op.fu == 'PA')|(tipo_op.fu == 'RR')|(tipo_op.fu == 'RO')|(tipo_op.fu == 'AC')|(tipo_op.fu == 'TO')|(tipo_op.fu == 'AP')]
    nordeste = tipo_op[(tipo_op.fu == 'RN')|(tipo_op.fu == 'PB')|(tipo_op.fu == 'PE')|(tipo_op.fu == 'AL')|(tipo_op.fu == 'SE')|(tipo_op.fu == 'BA')|(tipo_op.fu == 'CE')|(tipo_op.fu == 'MA')|(tipo_op.fu == 'PI')]

    sudeste_group = sudeste.groupby('type_operation').count()
    sul_group = sul.groupby('type_operation').count()
    norte_group = norte.groupby('type_operation').count()
    centro_group = centro.groupby('type_operation').count()
    nordeste_group = nordeste.groupby('type_operation').count()

    transp_sudeste = sudeste_group.T
    transp_sudeste.reset_index(drop=True, inplace=True)

    transp_sul = sul_group.T
    transp_sul.reset_index(drop=True, inplace=True)

    transp_norte = norte_group.T
    transp_norte.reset_index(drop=True, inplace=True)

    transp_centro = centro_group.T
    transp_centro.reset_index(drop=True, inplace=True)

    transp_nordeste = nordeste_group.T
    transp_nordeste.reset_index(drop=True, inplace=True)

    df_ok = pd.DataFrame(columns=['AEROTAXI', 'AGRICULTURAL', 'EXPERIMENTAL', 'INSTRUCTION', 'NOT REGULAR', 'POLICIAL', 'PRIVATE', 'REGULAR', 'SPECIALIZED'])
    df_ok

    df_ok = df_ok.append(transp_sul, ignore_index=True)
    df_ok = df_ok.append(transp_sudeste, ignore_index=True)
    df_ok = df_ok.append(transp_norte, ignore_index=True)
    df_ok = df_ok.append(transp_nordeste, ignore_index=True)
    df_ok = df_ok.append(transp_centro, ignore_index=True)

    df_ok.loc[4, ['NOT REGULAR']] = 0

    df_ok['TOTAL'] = df_ok['AEROTAXI'] + df_ok['EXPERIMENTAL'] + df_ok['INSTRUCTION'] + df_ok['NOT REGULAR'] + df_ok['POLICIAL'] + df_ok['PRIVATE'] + df_ok['REGULAR'] + df_ok['SPECIALIZED']

    regioes = gpd.read_file('regioes_2010.shp')
    completo = pd.concat([regioes, df_ok], axis=1)
    regioes_geo = regioes.to_json()

    crs = {'init': 'epsg:4326'}
    regioes.to_crs(crs, inplace=True)

    #Coordenadas x e y do centro do Brasil
    y = regioes.centroid.y.iloc[0]+12
    x = regioes.centroid.x.iloc[0]

    #Plotando a base do mapa
    base = folium.Map([y, x], zoom_start=4, tiles='OpenStreetMap')

    #Plotar cores de cada região
    folium.Choropleth(
        geo_data=regioes_geo,
        name='choropleth',
        data=completo,
        columns=['nome', 'TOTAL'],
        key_on='feature.properties.nome',
        fill_color='YlGn',
        fill_opacity=0.9,
        line_opacity=0.2,
        legend_name='Quantidade de acidentes por região'
    ).add_to(base)


    #Plotando uma camada para cada região do Brasil
    for i in range(len(completo)):
        style1 = {'color': 'red'}
        geo = folium.GeoJson(completo[i:i+1], name=completo['nome'][i], style_function=lambda x: {'fillColor': '#FF000000', 'color': 'black', 'weight': 0.5}) #Pegando cada linha do dataframe e atribuindo um nome a ela
        label = "<h4>" + str(completo['nome'][i]) + "<\h4> <\h5> Total: " + str(completo['TOTAL'][i]) + "<\h5> <h6> Aerotáxi: " +str(completo['AEROTAXI'][i])+ "<\h6> <h6> Agricultura: " +str(completo['AGRICULTURAL'][i])+ "<\h6> <h6> Experimental: "+str(completo['EXPERIMENTAL'][i])+ "<\h6> <h6> Instrução: "+str(completo['INSTRUCTION'][i])+ "<\h6> <h6> Irregular: "+str(completo['NOT REGULAR'][i])+ "<\h6> <h6> Policial: "+str(completo['POLICIAL'][i])+ "<\h6> <h6> Privado: "+str(completo['PRIVATE'][i])+ "<\h6> <h6> Regular: "+str(completo['REGULAR'][i])+ "<\h6> <h6> Especializado: "+str(completo['SPECIALIZED'][i])+ "<\h6>"
        folium.Popup(label, max_width=300).add_to(geo) #Adicionando o popup àquela camada
        geo.add_to(base) #Adicionando a camada na base

    st_data = folium_static(base, width=1000)


def grafico_estados(dados, Estados):
    #Gerando um dataframe com as colunas dos Estados, 'fu', e o identificador da ocorrência, 'occurrence_id'.
    estados = dados[["fu","occurrence_id"]]

    #Removendo informações inconsistentes:
    estados = estados[estados.fu!='***']

    #Agrupando os dados com base na coluna de Estados.
    estados = estados.groupby('fu').count()
    estados.reset_index(inplace=True) #Reorganizando os índices

    #Trocando as siglas dos Estados pelos seus nomes, objetivando facilitar o merge com o dataframe do IBGE.
    estados.loc[estados.fu=='AC', 'fu'] = 'ACRE'
    estados.loc[estados.fu=='AL', 'fu'] = 'ALAGOAS'
    estados.loc[estados.fu=='AM', 'fu'] = 'AMAZONAS'
    estados.loc[estados.fu=='AP', 'fu'] = 'AMAPÁ'
    estados.loc[estados.fu=='BA', 'fu'] = 'BAHIA'
    estados.loc[estados.fu=='CE', 'fu'] = 'CEARÁ'
    estados.loc[estados.fu=='DF', 'fu'] = 'DISTRITO FEDERAL'
    estados.loc[estados.fu=='ES', 'fu'] = 'ESPÍRITO SANTO'
    estados.loc[estados.fu=='GO', 'fu'] = 'GOIÁS'
    estados.loc[estados.fu=='MA', 'fu'] = 'MARANHÃO'
    estados.loc[estados.fu=='MG', 'fu'] = 'MINAS GERAIS'
    estados.loc[estados.fu=='MS', 'fu'] = 'MATO GROSSO DO SUL'
    estados.loc[estados.fu=='MT', 'fu'] = 'MATO GROSSO'
    estados.loc[estados.fu=='PA', 'fu'] = 'PARÁ'
    estados.loc[estados.fu=='PB', 'fu'] = 'PARAÍBA'
    estados.loc[estados.fu=='PE', 'fu'] = 'PERNAMBUCO'
    estados.loc[estados.fu=='PI', 'fu'] = 'PIAUÍ'
    estados.loc[estados.fu=='PR', 'fu'] = 'PARANÁ'
    estados.loc[estados.fu=='RJ', 'fu'] = 'RIO DE JANEIRO'
    estados.loc[estados.fu=='RN', 'fu'] = 'RIO GRANDE DO NORTE'
    estados.loc[estados.fu=='RO', 'fu'] = 'RONDÔNIA'
    estados.loc[estados.fu=='RR', 'fu'] = 'RORAIMA'
    estados.loc[estados.fu=='RS', 'fu'] = 'RIO GRANDE DO SUL'
    estados.loc[estados.fu=='SC', 'fu'] = 'SANTA CATARINA'
    estados.loc[estados.fu=='SE', 'fu'] = 'SERGIPE'
    estados.loc[estados.fu=='SP', 'fu'] = 'SÃO PAULO'
    estados.loc[estados.fu=='TO', 'fu'] = 'TOCANTINS'
    estados.rename(columns={'occurrence_id':'Quantidades', 'fu':'NM_ESTADO'}, inplace=True) #Trocando os nomes das colunas para se realizar o merge.

    mapa = pd.merge(Estados, estados,  how='inner', on=['NM_ESTADO']) #Merge entre os dataframes do IBGE e o gerado na célula anterior.

    Estados_geo = estados_geo(Estados)

    crs = {'init': 'epsg:4326'}
    mapa.to_crs(crs, inplace=True)

    #Coordenadas x e y do centro do Brasil
    y = mapa.centroid.y.iloc[0]-4
    x = mapa.centroid.x.iloc[0]+12

    #Plotando a base do mapa
    base = folium.Map([y, x], zoom_start=4, tiles='OpenStreetMap')

    #Plotar cores de cada região
    folium.Choropleth(
        geo_data=Estados_geo,
        name='choropleth',
        data=mapa,
        columns=['NM_ESTADO', 'Quantidades'],
        key_on='feature.properties.NM_ESTADO',
        fill_color='OrRd',
        fill_opacity=0.9,
        line_opacity=0.2,
        legend_name='Quantidade de acidentes por estado'
    ).add_to(base)


    #Plotando uma camada para cada região do Brasil
    for i in range(len(mapa)):
        style1 = {'color': 'red'}
        geo = folium.GeoJson(mapa[i:i+1], name=mapa['NM_ESTADO'][i], style_function=lambda x: {'fillColor': '#FF000000', 'color': 'black', 'weight': 0.5}) #Pegando cada linha do dataframe e atribuindo um nome a ela
        label = "<h4>" + str(mapa['NM_ESTADO'][i]) + "<\h4> <\h5> Quantidade de acidentes: " + str(mapa['Quantidades'][i]) + "<\h5>" 
        folium.Popup(label, max_width=300).add_to(geo) #Adicionando o popup àquela camada
        geo.add_to(base) #Adicionando a camada na base

    st_data = folium_static(base, width=1000)

@st.cache
def estados_geo(Estados):
    e = Estados.to_json()
    return e



def mostra_graficos_espaciais(dados, Estados):
    grafico_regiao(dados, Estados)
    grafico_estados(dados, Estados)
