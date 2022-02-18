from .parser_base import Parser
from ..utilities import sync_to_async

import asyncio
from bs4 import BeautifulSoup
from typing import List, Dict


class CryptoPotato(Parser):
  ''' cryptopotato.com module'''

  BASE_URL = 'http://cryptopotato.com'
  NEWS_URL = 'https://cryptopotato.com/crypto-news/page/{page}/'

  def url(self, page: int) -> str:
    page = 0 if page == 1 else page
    return self.NEWS_URL.format(page=page)

  async def parse(self, count: int) -> List[Dict[str, str]]:
    articles_url, page = list(), 1

    while len(articles_url) < count:
      response = await self.requests_session.get(self.url(page))
      html_code = response.text

      articles = await self.__parse_articles(html_code)
      articles_url = [*articles_url, *articles]
      page += 1

    result = await asyncio.gather(*[
      self.parse_article(article_url)
    for article_url in articles_url[:count]])

    return result

  async def parse_article(self, url: str) -> Dict[str, str]:
    response = await self.requests_session.get(url)
    html_code = response.text
    return await self.__parse_article(html_code)

  @sync_to_async
  def __parse_articles(self, html_code: str) -> List[str]:
    parser = BeautifulSoup(html_code, 'html.parser')
    articles = parser.find(id='list-items').find_all('article')

    result = [
      article.find('h3').find('a').get('href')
    for article in articles if self.check_keywords(article.find('h3').text, article.find(class_='entry-excerpt').text)]

    return result

  @sync_to_async
  def __parse_article(self, html_code: str) -> Dict[str, str]:
    result = dict()
    parser = BeautifulSoup(html_code, 'html.parser')

    result['language'] = parser.find('html').get('lang').split('-')[0]
    result['title'] = parser.find('h1').text.strip()
    result['text'] = '\n'.join(text.text.strip() for text in parser.find(class_='coincodex-content').find_all('p', recursive=False))
    result['date'] = parser.find(class_='last-modified-timestamp').text.strip()
    result['source'] = self.BASE_URL

    return result
