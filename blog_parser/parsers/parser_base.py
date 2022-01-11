from abc import ABC, abstractmethod
from typing import Sequence, AnyStr


class Parser(ABC):
  ''' an Abstract class for parsing modules '''

  BASE_URL: AnyStr
  NEWS_URL: AnyStr

  def __init__(self, requests_session, keywords: Sequence[AnyStr]) -> None:
      self.requests_session, self.keywords = requests_session, keywords

  @abstractmethod
  def parse(self) -> None:
    ''' Method to parse news with the representation of JSON '''
    pass