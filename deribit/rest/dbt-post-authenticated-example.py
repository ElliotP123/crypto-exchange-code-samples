"""
Description:
    Deribit RESToverHTTP [POST] Asyncio Example.

    - Authenticated request.

Usage:
    python3.9 dbt-post-authenticated-example.py

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
    client_secret: str,
    payload: Dict
        ) -> None:

    async with aiohttp.ClientSession() as session:
        async with session.post(
            connection_url+endpoint,
            auth=BasicAuth(client_id, client_secret),
            json=payload
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
    endpoint: str = 'private/buy'

    # DBT Client ID
    client_id: str = '<client-id>'
    # DBT Client Secret
    client_secret: str = '<client-secret>'

    # DBT [POST] RESToverHTTP Payload
    payload: Dict = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "private/buy",
                    "params": {
                        "instrument_name": "BTC-PERPETUAL",
                        "amount": 500,
                        "type": "market",
                        "label": "tester"
                        }
                    }

    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    loop.run_until_complete(
        main(
            connection_url=connection_url,
            endpoint=endpoint,
            client_id=client_id,
            client_secret=client_secret,
            payload=payload
            )
        )
