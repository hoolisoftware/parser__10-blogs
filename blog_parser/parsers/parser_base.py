from httpx import AsyncClient
from abc import ABC, abstractmethod
from typing import Sequence, AnyStr, List, Dict


class Parser(ABC):
  ''' an Abstract class for parsing modules '''

  BASE_URL: AnyStr
  NEWS_URL: AnyStr

  def __init__(self, requests_session: AsyncClient, keywords: Sequence[AnyStr]) -> None:
      self.requests_session, self.keywords = requests_session, keywords

  @abstractmethod
  async def parse(self, count: int) -> List[Dict[str, str]]:
    ''' Method to parse news with the representation of JSON '''
    pass
