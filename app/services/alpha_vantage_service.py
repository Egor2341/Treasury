from fastapi import HTTPException

from adapters.alpha_vantage_adapter import AlphaVantageAdapter

import asyncio
import time

from models.info.exchange import ExchangeDto


async def retry(func, retries=3):
    for i in range(retries):
        try:
            return await func()
        except Exception:
            if i == retries - 1:
                raise
            await asyncio.sleep(1)


class RateLimiter:
    def __init__(self, max_calls=5, period=60):
        self.max_calls = max_calls
        self.period = period
        self.calls = []

    def allow(self):
        now = time.time()
        self.calls = [t for t in self.calls if now - t < self.period]

        if len(self.calls) >= self.max_calls:
            return False

        self.calls.append(now)
        return True


class ExchangeService:

    def __init__(self):
        self.adapter = AlphaVantageAdapter()
        self.limiter = RateLimiter()

    async def _fetch_rate(self, currency: str):
        if not self.limiter.allow():
            raise HTTPException(status_code=429, detail="Rate limit exceeded")

        data = await retry(lambda: self.adapter.get_rate(currency, "RUB"))

        try:
            raw = data["Realtime Currency Exchange Rate"]
            return float(raw["5. Exchange Rate"])
        except KeyError:
            raise Exception("Invalid API response")

    async def get_rates(self) -> ExchangeDto:
        currencies = ["USD", "EUR", "CNY"]

        result = {}
        for cur in currencies:
            result[cur] = await self._fetch_rate(cur)

        return ExchangeDto(
            usd=result["USD"],
            eur=result["EUR"],
            cny=result["CNY"]
        )
