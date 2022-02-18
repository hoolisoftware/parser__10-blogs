from .parser_base import Parser
from ..utilities import sync_to_async

import asyncio
from bs4 import BeautifulSoup
from typing import List, Dict


class Happycoin(Parser):
  ''' happycoin.club module '''

  BASE_URL = 'https://happycoin.club'
  NEWS_URL = 'https://happycoin.club/cryptocurrencies-news/'

  def url(self, page: int) -> str:
    return self.NEWS_URL if page == 1 else self.NEWS_URL + f'page/{page}/'

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
    articles = parser.find_all(class_='grid-list-content col-lg-4 equal')

    result = [
      article.find('h4').find('a').get('href')
    for article in articles if self.check_keywords(article.find('h4').text)]

    return result

  @sync_to_async
  def __parse_article(self, html_code: str) -> Dict[str, str]:
    result = dict()
    parser = BeautifulSoup(html_code, 'html.parser')

    result['language'] = parser.find('html').get('lang').split('-')[0]
    result['title'] = parser.find('h1').text.strip()
    result['text'] = '\n'.join(text.text.strip() for text in parser.find(class_='single-post-content').find_all('p')).replace('Ваш адрес email не будет опубликован. Обязательные поля помечены *', '').replace('Редактор. Переводчик. Криптоинвестор.', '').strip()
    result['date'] = parser.find(class_='content-date date pull-left').text.split(' | ')[0].strip()
    result['source'] = self.BASE_URL

    return result
