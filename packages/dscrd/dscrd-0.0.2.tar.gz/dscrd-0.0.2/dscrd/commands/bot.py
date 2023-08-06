import opcode
import requests
import random
import time
import json
import asyncio
import websockets
from multiprocessing import Process

class Bot:
    def __init__(self, token: str, intents: int = None, name: str = ""):
        self.token = token
        self.headers = {
            "Authorization": f"Bot {token}"
        }
        self.ws = None
        self.hello = {"op": 1, "d": None}
        self.delay = 0
        self.interval = 0
        self.seq_num = None
        self.resume_url = None
        self.session_id = None
        self.intents = intents
        self.name = name

    def get_gateway(self):
        return requests.get("https://discord.com/api/v10/gateway/bot", headers=self.headers)

    async def start_bot(self):
        gateway = requests.get("https://discord.com/api/v10/gateway/bot", headers=self.headers)
        #self.ws = create_connection(gateway.json()["url"] + "?v=10&encoding=json")
        async with websockets.connect(gateway.json()["url"] + "?v=10&encoding=json") as websocket:
            self.ws = websocket
            gateway_hello = await self.ws.recv()
            gateway_hello = json.loads(gateway_hello)
            # wait for a certain amount of milliseconds
            # wait for the heartbeat_interval in "d" in gateway_hello + jitter milliseconds
            self.interval = gateway_hello["d"]["heartbeat_interval"] / 1000
            self.delay = self.interval
            self.hello["d"] = self.seq_num
            # wait for the delay in milliseconds
            await self.identify()
            task = asyncio.create_task(self.send())
            await asyncio.gather(self.listen(), task)

    async def identify(self):
        identify_message = {
            "op": 2,
            "d": {
                "token": self.token,
                "intents": int(self.intents),
                "properties": {
                    "os": "windows",
                    "browser": self.name,
                    "device": self.name
                }
            }
        }
        # encode the identify_message to a string
        identify_message = json.dumps(identify_message)
        await self.ws.send(identify_message)
        response = await self.ws.recv()
        # decode the byte array to a string
        # decode the string to a json object
        response = json.loads(response)
        self.session_id = response["d"]["session_id"]
        self.resume_url = response["d"]["resume_gateway_url"]

    async def send(self):
        jitter = random.random()
        await asyncio.sleep(jitter / 1000)
        await asyncio.sleep(self.delay)
        await self.ws.send(json.dumps(self.hello))
        current_time = time.time()
        while True:
            try:
                if self.delay <= 0:
                    await self.ws.send(json.dumps(self.hello))
                    self.delay = self.interval
                else:
                    self.delay -= ((time.time() - current_time) * 1000)
                    current_time = time.time()
            except:
                await self.resume_connection()
                break
        
    async def listen(self):
        response = await self.ws.recv()
        response = json.loads(response)
        opcode = response["op"]
        while opcode == 11 or opcode == 1:
            try:
                response = await self.ws.recv()
                response = json.loads(response)
                # check if the response has an opcode

                opcode = response["op"]
                if opcode == 1:
                    await self.ws.send(json.dumps(self.hello))
                    self.delay = self.interval
                    self.seq_num = response["d"]["seq"]

                elif opcode == 7:
                    await self.resume_connection()

                elif opcode == 9:
                    is_resumaable = response["d"]
                    if is_resumaable:
                        self.resume_connection()
                    else:
                        await self.ws.wait_closed(1001)
                        self.loop.stop()
                        self.loop.close()
                        self.start_bot()

                elif opcode == 11:
                    self.seq_num = response["d"]["seq"]
                    self.delay = self.interval

                else:
                    print(response)
                    
            except:
                await self.resume_connection()
                break

    async def resume_connection(self):
        await self.ws.wait_closed()
        gateway_resume = {
            "op": 6,
            "d": {
                "token": self.token,
                "session_id": self.session_id,
                "seq": self.seq_num
            }
        }
        gateway_resume = json.dumps(gateway_resume)
        async with websockets.connect(self.resume_url) as websocket:
            self.ws = websocket
        await self.ws.send(gateway_resume)
        response = await self.ws.recv()
        response = json.loads(response)
        opcode = response["op"]
        # check if the response is 9, if it is, there was an error
        if opcode == 9:
            is_resumaable = response["d"]
            if is_resumaable == True:
                await self.resume_connection()
        else:
            self.seq_num = response["d"]["seq"]
            self.delay = self.interval
            task = asyncio.create_task(self.send())
            await asyncio.gather(self.listen(), task)