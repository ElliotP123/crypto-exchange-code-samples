"""
Description:
    Deribit RESToverHTTP [GET] Asyncio Example.

    - Unauthenticated request.

Usage:
    python3.9 dbt-unauthenticated-example.py

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

    # DBT LIVE RESToverHTTP Connection URL
    # connection_url: str = 'https://www.deribit.com/api/v2/'
    # DBT TEST RESToverHTTP Connection URL
    connection_url: str = 'https://test.deribit.com/api/v2/'

    # DBT RESToverHTTP Endpoint + Query String Parameter(s)
    endpoint: str = 'public/get_instruments?currency=BTC'

    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    loop.run_until_complete(
        main(
            connection_url=connection_url,
            endpoint=endpoint
            )
        )
