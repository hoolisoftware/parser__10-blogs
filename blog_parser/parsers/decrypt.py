from .parser_base import Parser

from bs4 import BeautifulSoup
from typing import List, Dict


class Decrypt(Parser):
  ''' decrypt.co module '''

  BASE_URL = 'https://decrypt.co',
  NEWS_URL = 'https://api.decrypt.co/content-elasticsearch/posts'

  def payload(self, offset: int) -> dict:
    return {
      '_minimal': True,
      'category': 'news',
      'lang': 'en-US',
      'offset': offset,
      'order': 'desc',
      'orderby': 'date',
      'per_page': 12,
      'type': 'post'
    }

  async def parse(self, count: int) -> List[Dict[str, str]]:
    result, offset = list(), 0

    while len(result) < count:
      offset_alter = 0
      response = await self.requests_session.get(self.NEWS_URL, params=self.payload(offset))
      for article in response.json():
        offset_alter += 1
        if self.check_keywords(article['title']['rendered'], article['excerpt']['rendered']):

          result.append({
            'language': 'en',
            'title': self.decode(article['title']['rendered']),
            'text': self.decode(article['content']['rendered']),
            'date': article['date']
          })

      offset += offset_alter

    return result[:count]

  async def parse_article(self, url: str) -> Dict[str, str]:
    return await super().parse_article(url)

  def decode(self, string: str) -> str:
    return BeautifulSoup(string, 'html.parser').text
