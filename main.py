import sys
import requests
import pandas as pd
import json
from bs4 import BeautifulSoup

#Função que obtém a duração do filme
def get_duration_movie(url):

    req_url = requests.get(url)

    try:
       req_url.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise SystemExit(error) 

    initial_soup_duration = BeautifulSoup(req_url.text, 'html.parser')
    initial_raw_duration = initial_soup_duration.find('textarea', id='paste_code').text

    soup_duration = BeautifulSoup(initial_raw_duration,'html.parser')
    raw_duration = soup_duration.findAll('dd')[1].string
    
    return raw_duration

def get_movie_info(listing_url: str, links_url: str, movie_id: str):

    #Obtendo a categoria e o título do filme repassada nos parâmetros
    category,title = movie_id.split('/')
        
    #Obtendo tabela que contém os dados dos filmes
    req_listing = requests.get(listing_url)

    try:
       req_listing.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise SystemExit(error)

    initial_soup_listing = BeautifulSoup(req_listing.text, 'html.parser')
    initial_raw_listing = initial_soup_listing.find('textarea', id='paste_code').text

    soup_listing = BeautifulSoup(initial_raw_listing, 'html.parser')
    raw_listing = soup_listing.find('table',class_='highlight')

    table_listing = pd.read_html(str(raw_listing))

    #Obtendo tabela que contém o link do filme
    req_links = requests.get(links_url)

    try:
       req_links.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise SystemExit(error)

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

    #Retirando coluna nome do filme duplicada
    df_merge = df_merge.loc[:,~df_merge.T.duplicated(keep='first')]

    #Renomeando coluna do DataFrame unificado
    df_merge = df_merge.rename(columns={'nome_x':'title', 'genero':'category', 'diretor':'director', 'url':'link'})

    #Reorganizando as colunas
    df_merge = df_merge.reindex(columns=['id','link','title','category','director'])

    #Selecionando os dados no DataFrame de acordo com o parâmetro movie_id repassado
    row_movie = df_merge.loc[(df_merge['title']==title) & (df_merge['category']==category)]

    if len(row_movie) == 0:
        raise SystemError('Movie id not found')

    #Seleciona os valores da linha selecionada
    row_movie_values = row_movie.values

    #Cria parte do dicionário
    for i in row_movie_values:
        dic = {}
        dic['url'] = i[1]
        dic['titulo'] = i[2]
        dic['genero'] = i[3]
        dic['diretor'] = i[4]    

    #Função que retorna a duração do filme 
    duration = get_duration_movie(dic['url'])

    #Adiciona a duração do filme no dicionário
    dic['duracao'] = duration
    
    #Exibe o dicionário
    print(json.dumps(dic,indent=4))

def main():
    if len(sys.argv) < 2:
        raise SystemError('Invalid numbers of arguments')
    else:
        get_movie_info('https://pastebin.com/PcVfQ1ff', 'https://pastebin.com/Tdp532rr', sys.argv[1]+'/'+' '.join(sys.argv[2:]))

if __name__ == "__main__":
    main()