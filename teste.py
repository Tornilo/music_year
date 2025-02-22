import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
#Procurar música no Spotify
def buscar_musica_spotify(nome_musica, nome_artista, client_id, client_secret):
    
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
    
    query = f"track:{nome_musica} artist:{nome_artista}"
    resultado = sp.search(q=query, type="track", limit=1)
    
    if resultado['tracks']['items']:
        link = resultado['tracks']['items'][0]['external_urls']['spotify']
        return link
    else:
        return "Música não encontrada."

# Ler um arquivo CSV
df = pd.read_csv('list_song_billboard.csv')

st.title("Descubra a música que estava no top 10 do Billboard")
year = st.number_input("Digite o ano:", min_value=1958, max_value=2025, value=2025, step=1)
month = st.number_input("Digite mês:", min_value=1, max_value=31, value=1, step=1)

if st.button('Buscar músicas'):

    # Converter a coluna 'Date' para o tipo datetime
    df['chart_week'] = pd.to_datetime(df['chart_week'])

    # Filtrar por mês e ano (exemplo: outubro de 2023)
    filtered_df = df[(df['chart_week'].dt.month == month) & (df['chart_week'].dt.year == year)]

    # Selecionar as 10 primeiras linhas
    top_10 = filtered_df.head(10)
    i =0

    # Loop para ler 'Title' e 'Artist' de cada linha
    for index, row in top_10.iterrows():
        i+=1
        title = row['title']
        artist = row['performer']
        link = buscar_musica_spotify(title, artist, client_id, client_secret)
        st.write(f"{i} - {title}, {artist}: [Ouvir no Spotify]({link})")