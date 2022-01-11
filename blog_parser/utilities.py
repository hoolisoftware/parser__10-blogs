import asyncio
from typing import Callable, Tuple, Dict, Any


def sync_to_async(function: Callable) -> Callable:
  ''' Wrap sync tasks (like paring) into async '''

  async def wrapper(*args: Tuple[Any], **kwargs: Dict[Any, Any]) -> Any:
    return await asyncio.to_thread(function, *args, **kwargs)

  return wrapper
