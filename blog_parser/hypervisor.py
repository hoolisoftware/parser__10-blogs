from .parsers import Parser
from .requests_session import RequestsSession

import sys
import asyncio

from os import environ
from base64 import b64encode

from functools import reduce
from typing import Sequence, AnyStr, Tuple, List, Dict


class HyperVisor:
  ''' a Class for hypervisoring all parser modules '''

  def __init__(self, keywords: Sequence[AnyStr], *parser_classes: Tuple[Parser]) -> None:
    self.parser_classes, self.parsers = parser_classes, None
    self.requests_session_class = RequestsSession()
    self.keywords = keywords

    try:
      wp_login = environ['WP_LOGIN']
      wp_password = environ['WP_PASSWORD']
      self.wp_url = environ['WP_URL']
    except KeyError:
      print('Environment variables WP_LOGIN and WP_PASSWORD missing')
      sys.exit(0)

    token = b64encode(f'{wp_login}:{wp_password}'.encode()).decode()
    self.headers = {'Authorization': f'Basic {token}'}

  async def close(self) -> None:
    await self.requests_session_class.close_requests_session()

  async def initialize(self) -> None:
    requests_session = await self.requests_session_class.get_requests_session(self.headers)

    self.parsers: List[Parser] = [
      parser_class(requests_session, self.keywords)
    for parser_class in self.parser_classes]

  async def parse(self, count: int) -> List[Dict[str, str]]:
    load = self.__get_load(count, len(self.parsers))

    results = await asyncio.gather(*[
      parser_class.parse(its_load)
    for parser_class, its_load in zip(self.parsers, load)])

    return list(reduce(lambda a, x: a + x, results))

  def __get_load(self, total: int, count: int) -> List[int]:
    divided = total // count
    load = [divided] * count

    if total % count != 0:
      counter = -1

      while sum(load) != total:
        load[(counter := counter + 1)] += 1

    return load

  async def run(self, count: int) -> int:
    sent_count = 0
    requests_session = await self.requests_session_class.get_requests_session(self.headers)

    for article in await self.parse(count):
      sent_count += 1

      payload = {
        'title': article['title'].strip(),
        'content': article['text'].strip(),
        'status': 'draft'
      }

      await requests_session.post(self.wp_url, json=payload)

    return sent_count
