#! python3

from blog_parser.parsers import *
from blog_parser import KEYWORDS, HyperVisor

import asyncio

COUNT = 1  # Count to parse


async def main() -> None:
  hypervisor = HyperVisor(KEYWORDS, BlockChain24, TakeProfit, BitcoinTalk, Cryptor, Happycoin, TtrCoin, CoinSpot)
  await hypervisor.initialize()

  await hypervisor.run(COUNT)
  print(f'Sent {COUNT} articles')
  await hypervisor.close()


if __name__ == '__main__':
  asyncio.run(main())
