import httpx

from config import settings


class AlphaVantageAdapter:

    async def get_rate(self, from_currency: str, to_currency: str):
        try:
            async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
                response = await client.get(
                    settings.alpha_vantage_url,
                    params={
                        "function": "CURRENCY_EXCHANGE_RATE",
                        "from_currency": from_currency,
                        "to_currency": to_currency,
                        "apikey": settings.alpha_vantage_api_key,
                    }
                )

                response.raise_for_status()
                return response.json()

        except httpx.TimeoutException:
            raise Exception("Timeout from Alpha Vantage")

        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP error: {e.response.status_code}")