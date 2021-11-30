"""
Description:
    Deribit RESToverHTTP [GET] Asyncio Example.

    - Authenticated request.

Usage:
    python3.9 dbt-authenticated-example.py

Requirements:
    - aiohttp >= 3.8.1
"""

# built ins
import asyncio
import logging
from typing import Dict

# installed
import aiohttp
from aiohttp.helpers import BasicAuth


async def main(
    connection_url: str,
    endpoint: str,
    client_id: str,
    client_secret: str
        ) -> None:

    async with aiohttp.ClientSession() as session:
        async with session.get(
            connection_url+endpoint,
            auth=BasicAuth(client_id, client_secret)
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
    endpoint: str = 'private/get_positions?currency=ETH'

    # DBT Client ID
    client_id: str = '<client-id>'
    # DBT Client Secret
    client_secret: str = '<client-secret>'

    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    loop.run_until_complete(
        main(
            connection_url=connection_url,
            endpoint=endpoint,
            client_id=client_id,
            client_secret=client_secret
            )
        )
