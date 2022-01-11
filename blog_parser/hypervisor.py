from .parsers import Parser
from .requests_session import RequestsSession

import asyncio
from functools import reduce
from typing import Sequence, AnyStr, Tuple, List, Dict


class HyperVisor:
  ''' a Class for hypervisoring all parser modules '''

  def __init__(self, keywords: Sequence[AnyStr], *parser_classes: Tuple[Parser]) -> None:
    self.parser_classes, self.parsers = parser_classes, None
    self.requests_session_class = RequestsSession()
    self.keywords = keywords

  async def close_requests_session(self) -> None:
    await self.requests_session_class.close()

  async def initialize(self) -> None:
    requests_session = await self.requests_session_class.get_requests_session()

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
    devided = total // count
    load = [devided] * count

    if total % count != 0:
      counter = -1

      while sum(load) != total:
        load[(counter := counter + 1)] += 1

    return load
