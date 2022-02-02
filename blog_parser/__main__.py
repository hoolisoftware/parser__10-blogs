from .hypervisor import HyperVisor
from .config import KEYWORDS, COUNT

from .parsers import (
  BlockChain24,
  TakeProfit,
  BitcoinTalk,
  Cryptor,
  Happycoin,
  TtrCoin,
  CoinSpot
)

import asyncio


async def main() -> None:
  hypervisor = HyperVisor(KEYWORDS, BlockChain24, TakeProfit, BitcoinTalk, Cryptor, Happycoin, TtrCoin, CoinSpot)
  await hypervisor.initialize()

  result = await hypervisor.parse(COUNT)
  print(*result, sep='\n\n')
  await hypervisor.close()


if __name__ == '__main__':
  asyncio.run(main())
