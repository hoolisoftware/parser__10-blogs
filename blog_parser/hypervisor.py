from .requests_session import RequestsSession
from typing import List


class HyperVisor:

  def __init__(self, parser_classes: List[object]) -> None:
    self.parser_classes, self.parsers = parser_classes, None
    self.requests_session_class = RequestsSession()

  async def initialize(self) -> None:
    requests_session = await self.requests_session_class.get_requests_session()

    self.parsers = [
      parser_class(requests_session)
    for parser_class in self.parser_classes]
