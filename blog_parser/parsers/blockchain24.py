

class BlockChain24:
  BASE_URL = 'https://blockchain24.pro/'
  NEWS_URL = 'https://blockchain24.pro/ajax/more_articles.php?category=3387'

  def __init__(self, requests_session) -> None:
      self.requests_session = requests_session
