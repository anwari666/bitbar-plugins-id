#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python3

import urllib.request as request
from bs4 import BeautifulSoup


def format_title( title, maxlen=60 ):
  """
  format a string with maximum string length
  maxlen defaults to 60.
  when it's more than 60, just replace the last 3 chars with periods
  """

  if len(title) > maxlen :
    return title[0:maxlen-3].ljust(maxlen, '.')
  else :
    return title.ljust(maxlen)

def print_articles( articles_soup ) :
  """ 
  input   : articles in bs4 soup
  output  : printed string
  """ 

  for article in articles_soup :
    title = None
    url = None
    
    title = article.find(['h1', 'h2'])
    url = article.find('a')

    if (title is not None) and (url is not None) :

      title = title.string.strip()
      url = url['href'].strip()

      # pretty print in terminal
      print( format_title(title), ' | href=', url )


def print_section(title, section_soup, level=0, limit=10) :
  """
  A method to print a whole section of articles, along with its title
  """
  articles = section_soup.find_all('article')
  print('### ', title, ' ###')
  print_articles( articles[0:limit] )


# ==== main thingy ===
def main() :

  print('CNN ID')
  print('---')
  response_body = None

  # Try to open the URL
  try:
    req = request.urlopen(url='https://www.cnnindonesia.com/')
    response_body = req.read() # the response's body
    
    # response_body = open('./cnnindonesia_201222_0624.html', 'r').read()

  except:
    print('Tydack bisa konek :(')

  if (response_body is not None) :

    soup = BeautifulSoup(response_body, 'html.parser')

    # === Berita Utama
    utama_soup = soup.find(id='slide_bu')
    print_section('UTAMA', utama_soup)


    # === TERPOPULER
    popular_soup = soup.find(class_='r_content').find(class_="box mb20")
    print_section('TERPOPULER', popular_soup)

    # === Headlines (id=headline is instance)
    headline_soup = soup.find(id='headline')
    print_section('HEADLINES', headline_soup)


    # === TERBARU
    latest_soup = soup.find(class_='berita_terbaru_lst')
    print_section('TERBARU', latest_soup)

main()