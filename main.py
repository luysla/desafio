import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_movie_info(listing_url, links_url):
    r = requests.get(listing_url)
    
    initial_soup = BeautifulSoup(r.text, 'html.parser')
    initial_raw = initial_soup.find('textarea', id='paste_code').text

    soup = BeautifulSoup(initial_raw, 'html.parser')

    raw = soup.find('table',class_='highlight')
    
    table = pd.read_html(str(raw))

    df_listing_url = pd.DataFrame(table[0])

get_movie_info('https://pastebin.com/PcVfQ1ff', 'https://pastebin.com/Tdp532rr')
