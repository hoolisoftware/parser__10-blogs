from .parser_base import Parser
from typing import Dict, List


class BlockChain24(Parser):
  ''' blockchain24.pro module '''

  BASE_URL = 'https://blockchain24.pro/'
  NEWS_URL = 'https://blockchain24.pro/ajax/more_articles.php?category=3387'

  async def parse(self, count: int) -> List[Dict[str, str]]:
    pass
