"""
Description:
    FTX WebSocket Asyncio Example.

    - Authenticated connection.

Usage:
    python3.9 ftx-ws-authenticated-example.py

Requirements:
    - websocket-client >= 1.2.1
"""

# built ins
import asyncio
import sys
import json
import logging
from typing import Dict
import time
import hmac

# installed
import websockets


class main:
    def __init__(
        self,
        ws_connection_url: str,
        access_key: str,
        secret_key: str
            ) -> None:
        # Async Event Loop
        self.loop = asyncio.get_event_loop()

        # Instance Variables
        self.ws_connection_url: str = ws_connection_url
        self.access_key: str = access_key
        self.secret_key: str = secret_key
        self.websocket_client: websockets.WebSocketClientProtocol = None

        # Start Primary Coroutine
        self.loop.run_until_complete(
            self.ws_manager()
            )

    async def ws_manager(self) -> None:
        async with websockets.connect(
            self.ws_connection_url,
            ping_interval=None,
            compression=None,
            close_timeout=60
            ) as self.websocket_client:

            # Authenticate WebSocket Connection
            await self.ws_auth()

            # Maintain Heartbeat
            self.loop.create_task(
                self.maintain_heartbeat()
                )

            # Subscribe to the specified WebSocket Channel
            self.loop.create_task(
                self.ws_operation(
                    operation='subscribe',
                    ws_channel='trades',
                    params='BTC-PERP'
                    )
                )

            while self.websocket_client.open:
                message: bytes = await self.websocket_client.recv()
                message: Dict = json.loads(message)
                logging.info(message)

                if 'type' in list(message):
                    if message['type'] in ['pong']:
                        continue

            else:
                logging.info('WebSocket connection has broken.')
                sys.exit(1)

    async def maintain_heartbeat(self) -> None:
        """
        Requests FTX's `op: ping` to maintain
        your WebSocket Connection.
        """
        msg: Dict = {
                    'op': 'ping'
                    }
        while True:
            await self.websocket_client.send(
                json.dumps(
                    msg
                    )
                )
            await asyncio.sleep(15)

    async def ws_auth(self) -> None:
        """
        Requests FTX's `op: login` to
        authenticate the WebSocket Connection.
        """
        # Create Signature with FTX API Credentials
        ts: int = int(time.time() * 1000)
        presign: str = f"{ts}websocket_login"
        sign: hmac = hmac.new(self.secret_key.encode(), presign.encode(), 'sha256').hexdigest()

        msg: Dict = {
                    "args": {
                        "key": access_key,
                        "sign": sign,
                        "time": ts
                    },
                    "op": "login"
                    }

        await self.websocket_client.send(
            json.dumps(
                msg
                )
            )

    async def ws_operation(
        self,
        operation: str,
        ws_channel: str,
        params: str = None
            ) -> None:
        """
        Requests `subscribe` or `unsubscribe`
        for FTX's WebSocket Channel
        """
        await asyncio.sleep(5)

        msg: Dict = {
                    'op': operation,
                    'channel': ws_channel,
                    'market': params
                    }

        await self.websocket_client.send(
            json.dumps(
                msg
                )
            )


if __name__ == "__main__":
    # Logging
    logging.basicConfig(
        level='INFO',
        format='%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
        )

    # FTX LIVE WebSocket Connection URL
    ws_connection_url: str = 'wss://ftx.com/ws/'

    # FTX Access Key
    access_key: str = '<access-key>'
    # FTX Secret Key
    secret_key: str = '<secret-key>'

    main(
         ws_connection_url=ws_connection_url,
         access_key=access_key,
         secret_key=secret_key
         )
