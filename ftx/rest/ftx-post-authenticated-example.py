"""
Description:
    FTX RESToverHTTP [POST] Asyncio Example.

    - Authenticated request.

Usage:
    python3.9 ftx-authenticated-example.py

Requirements:
    - aiohttp - 3.8.1
"""

# built ins
import asyncio
import json
import logging
from typing import Dict
import time
import hmac

# installed
import aiohttp


async def main(
    connection_url: str,
    endpoint: str,
    headers: Dict,
    payload: Dict
        ) -> None:

    async with aiohttp.ClientSession() as session:
        async with session.post(
            connection_url+endpoint,
            headers=headers,
            json=json.dumps(payload).encode('utf-8')
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
    connection_url: str = 'https://ftx.com/api/'

    # Request Method
    request_method: str = 'POST'

    # FTX RESToverHTTP Endpoint + Query String Parameter(s)
    endpoint: str = 'orders'

    # FTX [POST] RESToverHTTP Payload
    payload: Dict = {
        "market": "BTC-PERP",
        "side": "sell",
        "price": 65000,
        "type": "limit",
        "size": 15000.0,
        "reduceOnly": True,
        "ioc": False,
        "postOnly": False,
        "clientId": 'tester'
        }

    # FTX API Key
    api_key: str = '<api-key>'
    # FTX API Secret
    api_secret: str = '<api-secret>'

    # FTX Signature
    def create_headers(
        api_key: str,
        api_secret: str,
        request_method: str,
        endpoint: str,
        payload: Dict
            ) -> Dict:
        """
        Returns neccessary header payload
        for an authenticated FTX REST request.
        """
        ts: int = int(time.time() * 1000)

        signature_payload: bytes = f'{ts}{request_method}/api/{endpoint}'.encode()
        signature_payload += json.dumps(payload).encode()
        signature: hmac = hmac.new(api_secret.encode(), signature_payload, 'sha256').hexdigest()

        return {
                'FTX-KEY': api_key,
                'FTX-SIGN': signature,
                'FTX-TS': str(ts)
                }
    headers: Dict = create_headers(
        api_key=api_key,
        api_secret=api_secret,
        request_method=request_method,
        endpoint=endpoint,
        payload=payload
        )

    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    loop.run_until_complete(
        main(
            connection_url=connection_url,
            endpoint=endpoint,
            headers=headers,
            payload=payload
            )
        )
