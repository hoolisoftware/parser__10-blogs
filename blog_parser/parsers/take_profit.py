from .parser_base import Parser
from ..utilities import sync_to_async

import asyncio
from bs4 import BeautifulSoup
from typing import List, Tuple, Dict


class TakeProfit(Parser):
  ''' take-profit.org module '''

  BASE_URL = 'https://take-profit.org'
  NEWS_URL = 'https://take-profit.org/economicnews.php'

  async def parse(self, count: int) -> List[Dict[str, str]]:
    articles_url, page = list(), 1

    while len(articles_url) < count:
      response = await self.requests_session.get(self.NEWS_URL, params={'p': page})
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
    articles = parser.find_all(class_='material-block')

    result = [
      article.find(class_='material-title').get('href')
    for article in articles if self.check_keywords(article.find(class_='material-title').text)]

    return result

  @sync_to_async
  def __parse_article(self, html_code: str) -> Dict[str, str]:
    result = dict()
    parser = BeautifulSoup(html_code, 'html.parser')

    result['language'] = parser.find('html').get('lang')
    result['title'] = parser.find('h1').text
    result['text'] = '\n'.join(text.text.strip() for text in parser.find(class_='single-text').find_all('p'))
    result['date'] = parser.find(class_='statistic-date').text.strip()

    return result
