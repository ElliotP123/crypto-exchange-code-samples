"""
Description:
    BYB RESToverHTTP [GET] Asyncio Example.

    - Unauthenticated request.

Usage:
    python3.9 byb-get-unauthenticated-example.py

Requirements:
    - aiohttp >= 3.8.1
"""

# built ins
import asyncio
import logging
from typing import Dict

# installed
import aiohttp


async def main(
    connection_url: str,
    endpoint: str
        ) -> None:

    async with aiohttp.ClientSession() as session:
        async with session.get(
            connection_url+endpoint
                ) as response:
            # RESToverHTTP Status Code
            status_code: int = response.status
            logging.info(f'Response Status Code: {status_code}')

            # RESToverHTTP Response Content
            response: Dict = await response.json()
            logging.info(f'Response Content: {response}')


if __name__ == "__main__":
    # Logging
    logging.basicConfig(
        level='INFO'.upper(),
        format='%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
        )

    # FTX LIVE RESToverHTTP Connection URL
    # connection_url: str = 'https://api.bybit.com'
    # BYB TEST RESToverHTTP Connection URL
    connection_url: str = 'https://api-testnet.bybit.com'

    # BYB RESToverHTTP Endpoint + Query String Parameter(s)
    endpoint: str = '/v2/public/symbols'

    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    loop.run_until_complete(
        main(
            connection_url=connection_url,
            endpoint=endpoint
            )
        )
