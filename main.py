import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_duration_movie(url):
    print(url)

def get_movie_info(listing_url, links_url, movie_id):
    
    #Obtendo tabela que contém os dados dos filmes
    req_listing = requests.get(listing_url)
    initial_soup_listing = BeautifulSoup(req_listing.text, 'html.parser')
    initial_raw_listing = initial_soup_listing.find('textarea', id='paste_code').text

    soup_listing = BeautifulSoup(initial_raw_listing, 'html.parser')
    raw_listing = soup_listing.find('table',class_='highlight')

    table_listing = pd.read_html(str(raw_listing))

    #Obtendo tabela que contém o link do filme
    req_links = requests.get(links_url)
    initial_soup_links = BeautifulSoup(req_links.text, 'html.parser')
    initial_raw_links = initial_soup_links.find('textarea', id='paste_code').text

    soup_links = BeautifulSoup(initial_raw_links, 'html.parser')
    raw_links = soup_links.find('table',class_='highlight')

    table_links = pd.read_html(str(raw_links))

    #Criando DataFrame da tabela de listas dos filmes
    df_listing_url = pd.DataFrame(table_listing[0])

    #Criando DataFrame da tabela de links dos filmes
    df_links_url = pd.DataFrame(table_links[0]) 

    #Definindo ids nos DataFrames criados para unificar
    df_listing_url['id'] =  df_listing_url.index + 1
    df_links_url['id'] =  df_links_url.index + 1

    #Unificando DataFrame
    df_merge = pd.merge(df_listing_url, df_links_url, how='inner', on=['id', 'id'])

    #Retirando coluna duplicada
    df_merge = df_merge.loc[:,~df_merge.T.duplicated(keep='first')]

    #Renomeando coluna do DataFrame unificado
    df_merge = df_merge.rename(columns={'nome_x':'nome'})

    #Reorganizando as colunas
    df_merge = df_merge.reindex(columns=['id','nome','genero','diretor','link'])

    print(df_merge)
    
    #Obtendo a categoria e o nome do filme adicionada nos parâmetros
    category,name = movie_id.split('/')
    print (category, name)
    
get_movie_info('https://pastebin.com/PcVfQ1ff', 'https://pastebin.com/Tdp532rr', 'terror/a vila')
