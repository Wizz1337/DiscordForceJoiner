import asyncio, websockets, json, typing

InviteCode: str = 'gays'
Payload: dict = {"cmd":"INVITE_BROWSER","args":{"code":InviteCode},"nonce":"12c98f49-f5ad-4534-bb4a-466e9e92af21"}
livePort: int = 0000

async def jsonSend(ws, content: dict) -> None:
    await ws.send(json.dumps(content))

async def jsonRecv(ws) -> typing.Union[dict, None]:
    resp = await ws.recv()
    if resp:
        return json.loads(resp)

async def start(port: int) -> None:
    try:
        async with websockets.connect(f'ws://127.0.0.1:{port}/?v=1', extra_headers={'Origin': 'https://discord.com'}) as websocket:
            global livePort
            livePort = port
            while True:
                resp = await jsonRecv(websocket)
                if resp['evt'] == 'READY':
                    print(f'Successfully connected to ws://127.0.0.1:{port}/?v=1')
                    while True:
                        await jsonSend(websocket, Payload)
                        await asyncio.sleep(1)
    except ConnectionRefusedError:
        print(f'Connection failed to ws://127.0.0.1:{port}/?v=1')
        return
    except Exception as err:
        print(err)

for _ in range(6463, 6472):
    if livePort == 0000:
        asyncio.run(start(_))
    else:
        break

while True:
    asyncio.run(start(livePort))

