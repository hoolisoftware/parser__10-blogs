from httpx import AsyncClient
from fake_headers import Headers


class RequestsSession:
  ''' a Class for storing httpx.AsyncClient '''

  def __init__(self) -> None:
    self.requests_session: AsyncClient = None

  async def get_requests_session(self, headers: dict = {}) -> AsyncClient:
    headers = {**headers, **Headers().generate()}
    self.requests_session = self.requests_session or AsyncClient(headers=headers, timeout=5000)
    return self.requests_session

  async def close_requests_session(self) -> None:
    await self.requests_session.aclose()
