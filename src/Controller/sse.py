import asyncio
import json
import falcon
from falcon.asgi import SSEvent, WebSocket
from falcon import Response, Request
from redis import asyncio as aioredis

from utils.config import REDIS_URL

# class SeverSendEvent:
#     async def on_get(self, req: Request, resp: Response):
#         message_aio_connection = aioredis.ConnectionPool.from_url(REDIS_URL, db=13, decode_responses=True)
#         async def emmitter():
#             redist_pool = aioredis.Redis.from_pool(message_aio_connection)
#             pubsub = redist_pool.pubsub()
#             count = 0
#             await pubsub.subscribe("WenTee")
#             while True:
#                 await asyncio.sleep(0.2)
                
#                 message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1)
#                 if(message is None):
#                     continue
#                 data = json.loads(message['data'])
#                 print(data)
#                 yield SSEvent(
#                     json=data, retry=10000, event="connection"
#                 )


#         resp.content_type = "text/event-stream"
#         resp.sse = emmitter()

#     async def on_post(self, req: Request, resp: Response):
#         reqData = await req.get_media()
#         message_aio_connection = aioredis.ConnectionPool.from_url(REDIS_URL, db=13, decode_responses=True)
#         redis_pool = aioredis.Redis.from_pool(message_aio_connection)
#         await redis_pool.publish(
#             "WenTee",
#             json.dumps(reqData)
#         )

# class ChatAPI:
#     clients : set[WebSocket] = set()
#     async def on_websocket(self, req: Request, ws: WebSocket):
#         await ws.accept()
#         self.clients.add(ws)
#         print(len(self.clients))
#         try:
#             while True:
#                 data = await ws.receive_text()
#                 for client in self.clients:
#                     await client.send_text(data)
#         except falcon.WebSocketDisconnected as e:
#             self.clients.remove(ws)
#             print(len(self.clients))
#             print("disconnect")


    

