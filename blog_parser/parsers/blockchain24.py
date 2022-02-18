from .parser_base import Parser
from ..utilities import sync_to_async

import asyncio
from bs4 import BeautifulSoup
from typing import List, Tuple, Dict


class BlockChain24(Parser):
  ''' blockchain24.pro module '''

  BASE_URL = 'https://blockchain24.pro'
  NEWS_URL = 'https://blockchain24.pro/ajax/more_articles.php?category=3387'

  async def parse(self, count: int) -> List[Dict[str, str]]:
    articles_url, offset = list(), 1

    while len(articles_url) < count:
      response = await self.requests_session.get(self.NEWS_URL, params={'start_from': offset})
      html_code = response.text

      articles, articles_count = await self.__parse_articles(html_code)
      articles_url = [*articles_url, *articles]
      offset += articles_count

    result = await asyncio.gather(*[
      self.parse_article(article_url)
    for article_url in articles_url[:count]])

    return result

  async def parse_article(self, url: str) -> Dict[str, str]:
    response = await self.requests_session.get(url)
    html_code = response.text
    return await self.__parse_article(html_code)  

  @sync_to_async
  def __parse_articles(self, html_code: str) -> Tuple[List[str], int]:
    parser = BeautifulSoup(html_code, 'html.parser')
    articles = parser.find_all(class_='articles__block-item')
    articles_count = len(articles)

    result = [
      self.BASE_URL + article.find(class_='articles__block-item--header').get('href')
    for article in articles if self.check_keywords(article.find(class_='articles__block-item--header').text, article.find(class_='article-short-info').text)]

    return result, articles_count

  @sync_to_async
  def __parse_article(self, html_code: str) -> Dict[str, str]:
    result = dict()
    parser = BeautifulSoup(html_code, 'html.parser')

    result['language'] = parser.find('html').get('lang')
    result['title'] = parser.find(class_='article__header').text
    result['text'] = parser.find(class_='article__content').text.strip()
    result['date'] = parser.find(class_='article__info-date').text.strip()
    result['source'] = self.BASE_URL

    return result
