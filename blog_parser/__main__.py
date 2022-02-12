from .hypervisor import HyperVisor
from .config import KEYWORDS, COUNT

from .parsers import (
  BlockChain24,
  TakeProfit,
  BitcoinTalk,
  Cryptor,
  Happycoin,
  TtrCoin,
  CoinSpot,

  # Unused ones
  Decrypt,
  CryptoPotato
)

import time
import asyncio

import aioschedule
from datetime import datetime, timedelta


async def run(hypervisor: HyperVisor, count: int) -> None:
  sent_count = await hypervisor.run(count)
  print(f'Sent {sent_count} articles')
  

async def main() -> None:
  utc_h = datetime.utcnow().hour + 3  # Delta from UTC (Makes Moscow time if +3)
  now_h = datetime.now().hour
  delta = timedelta(hours=abs(utc_h - now_h))

  runtime = datetime(year=2000, month=1, day=1, hour=8, minute=0) + delta  # 08:00 no matter which timezone
  runtime = runtime.strftime('%H:%M')

  hypervisor = HyperVisor(KEYWORDS, BlockChain24, TakeProfit, BitcoinTalk, Cryptor, Happycoin, TtrCoin, CoinSpot)
  await hypervisor.initialize()

  aioschedule.every().day.at(runtime).do(run, hypervisor=hypervisor, count=COUNT)
  # await aioschedule.run_all()  # Use it to run out of schedule

  print(f'{COUNT} news everyday at {runtime}')

  while True:
    await aioschedule.run_pending()
    time.sleep(1)


if __name__ == '__main__':

  try:
    asyncio.run(main())
  except KeyboardInterrupt:
    print('\nGoodbye')
