from .parser_base import Parser
from ..utilities import sync_to_async

import asyncio
from bs4 import BeautifulSoup
from typing import List, Dict


class Cryptor(Parser):
  ''' cryptor.net module '''

  BASE_URL = 'https://cryptor.net'
  NEWS_URL = 'https://cryptor.net/news'

  async def parse(self, count: int) -> List[Dict[str, str]]:
    articles_url, page = list(), 0

    while len(articles_url) < count:
      response = await self.requests_session.get(self.NEWS_URL, params={'page': page})
      html_code = response.text

      articles = await self.__parse_articles(html_code)
      articles_url = [*articles_url, *articles]
      page += 1

    result = await asyncio.gather(*[
      self.parse_article(article_url)
    for article_url in articles_url][:count])

    return result

  async def parse_article(self, url: str) -> Dict[str, str]:
    response = await self.requests_session.get(url)
    html_code = response.text
    return await self.__parse_article(html_code)

  @sync_to_async
  def __parse_articles(self, html_code: str) -> List[str]:
    parser = BeautifulSoup(html_code, 'html.parser')
    articles = parser.find(class_='view-content').find_all('div', limit=1)

    result = [
      self.BASE_URL + article.find('a').get('href')
    for article in articles if self.check_keywords(article.find('a').text, article.find('header').next_sibling.text)]

    return result

  @sync_to_async
  def __parse_article(self, html_code: str) -> Dict[str, str]:
    result = dict()
    parser = BeautifulSoup(html_code, 'html.parser')

    result['language'] = parser.find('html').get('lang')
    result['title'] = parser.find('h1', class_='page-header').text.strip()
    result['text'] = parser.find('article').text.split('\n')[:-1][0].strip()
    result['date'] = parser.find(class_='autordate').find('span').text.split(', ')[1].split(' - ')[0]

    return result
