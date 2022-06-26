import pandas as pd
import geopandas as gpd
import streamlit as st

@st.cache
def tratamento():
    #Leitura do arquivo 'aircarfts' do github!
    url_aircrafts = 'https://github.com/alanldm/Ciencia_de_Dados/blob/6229bfc9bde193d7a11922bd5cfe6491c8633334/aircrafts.csv?raw=true'
    aircrafts = pd.read_csv(url_aircrafts, index_col=0, encoding='latin1')

    aircrafts = aircrafts.drop(columns=["fatalities_amount", "registration","operator_id","registration_country","registration_category","destination_flight","origin_flight","aircraft_id","extraction_day", "takeoff_max_weight (Lbs)", "seatings_amount"])

    #Leitura do arquivo 'occurrences' do github!
    url_occurrences = 'https://github.com/alanldm/Ciencia_de_Dados/blob/6229bfc9bde193d7a11922bd5cfe6491c8633334/occurrences.csv?raw=true'
    occurrences = pd.read_csv(url_occurrences, index_col=0, encoding='latin1')

    occurrences = occurrences[occurrences.country=='BRAZIL']
    occurrences = occurrences.drop(columns=["aircrafts_involved","recommendation_amount","investigation_status","under_investigation","classification","investigating_command", "country", "localization", "extraction_day","publication_day", "published_report", "report_number", "aerodrome", "takeoff"])

    #Leitura dos dados do IBGE:
    url_ibge = 'BRUFE250GC_SIR.shp'
    Estados = gpd.read_file(url_ibge)

    dados = pd.merge(aircrafts, occurrences, how='inner', on=['occurrence_id'])

    return dados, Estados