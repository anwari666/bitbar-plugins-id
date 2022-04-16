#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/bin/python3

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
  input   : articles in bs4 soup - only requires the title and url
  output  : printed string
  """ 

  for article in articles_soup :
    link = None
    
    link = article.find('a', class_="media__link")

    if (link is not None) :

      title = link.string.strip()
      url = link['href'].strip()

      # pretty print in terminal
      print( format_title(title), '| href='+url )


def print_articles_newsfeed(articles_soup) :
  """
  This function is special for detik's newsfeed
 
  input   : articles in bs4 soup
  output  : printed string
  """ 

  for article in articles_soup :
    title = None
    url = None
    
    title = article.find('div', class_="ai_replace_title")
    url = article

    if (title is not None) :

      title = title.string.strip()
      url = url['i-link'].strip()

      # pretty print in terminal
      print( format_title(title), '| href='+url )


def print_section(title, section_soup, level=0, limit=10) :
  """
  A method to print a whole section of articles, along with its title
  """
  articles = section_soup.find_all('article')
  print(title)
  print('---')
  print_articles( articles[0:limit] )



# ==== main function to call ===
def main() :

  print('dtk')
  print('---')
  response_body = None

  # Try to open the URL
  try:
    req = request.urlopen(url='https://www.detik.com/')
    response_body = req.read() # the response's body
    
    # alternatively, read from saved file
    # response_body = open('./detikcom_201227.html', 'r').read()

  except:
    print('Cannot connect :(')

  if (response_body is not None) :

    soup = BeautifulSoup(response_body, 'html.parser')

    # === Berita Populer
    popular_soup = soup.find(class_="box cb-mostpop")
    print_section('Berita Populer|href=#', popular_soup)


    # === News Feed
    feed_articles = soup.find_all('article', class_='ph_newsfeed_d')
    print('---')
    print('News Feed|href=#')
    print('---')
    print_articles_newsfeed(feed_articles)


# call the main program here
main()