from typing import Sequence, AnyStr


class BlockChain24:
  BASE_URL = 'https://blockchain24.pro/'
  NEWS_URL = 'https://blockchain24.pro/ajax/more_articles.php?category=3387'

  def __init__(self, requests_session, keywords: Sequence[AnyStr]) -> None:
      self.requests_session = requests_session
      self.keywords = keywords
