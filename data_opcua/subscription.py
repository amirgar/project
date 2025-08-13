import sys

sys.path.insert(0, "..")


import asyncio
import logging
import aiokafka
import json
from asyncua import Client, Node, ua
import datetime
from objprint import op

nds = []

async def rec(client: Client, cur_nod):
    if await cur_nod.get_children():
        for child in await cur_nod.get_children():
            if not await child.get_children():
                nds.append(child)
                # try:
                #     print(child, ": ", await child.read_value())
                # except Exception as e:
                #     print(f"{child}: No data")
            else:
                await rec(client, child)

def serializer(value):
    return json.dumps(value).encode()

def convert(s: str) -> list: 
    i = s[3]
    s = s.split(".")
    s[0] = s[0][7:]
    res = [f'{i}:{el}' for el in s]
    return res 

producer = None

async def prod():
    global producer
    producer = aiokafka.AIOKafkaProducer(
        bootstrap_servers=['10.0.2.22:9092'],
        value_serializer=serializer,
    )
    await producer.start()

class SubscriptionHandler:
    async def datachange_notification(self, node: Node, val, data):
        if val is not None and (await node.read_browse_name()).Name != 'CurrentTime':
            global producer
            try:
                # Extracting the VariantType
                message = {
                    "name": str((await node.read_browse_name()).Name),
                    "value": val,
                    "type": str(type(val)),  # Use the extracted VariantType
                    "ts": round(data.monitored_item.Value.ServerTimestamp.timestamp()),
                }
                # op(data.monitored_item.Value.ServerTimestamp)
                
                await producer.send_and_wait("data", message)
            except Exception as e:
                print(f"ERROR: {e}")

async def main():
    client = Client(url="opc.tcp://MrSmith:Doosan040100000*@10.194.2.38:49320")
    async with client:
        await prod()
        handler = SubscriptionHandler()
        subscription = await client.create_subscription(500, handler)
        root = await (client.get_objects_node()).get_child(convert("ns=2;i=0401000007_AVZ_NHP6300_OPC_UA"))
        await rec(client, root)
        await subscription.subscribe_data_change(nds)
        await asyncio.sleep(10000000)
        await subscription.delete()
        await asyncio.sleep(1)
    await producer.stop()  # Закрываем продюсер только после завершения работы

if __name__ == "__main__":
    asyncio.run(main())

"""
SELECT * 
FROM (
    SELECT 
        ROW_NUMBER() OVER (
            PARTITION BY window 
            ORDER BY count DESC
        ) AS row_number, 
        name, 
        value,  -- Добавляем value
        count
    FROM (
        SELECT 
            name, 
            value,
            hop(INTERVAL '10' SECOND, INTERVAL '5' HOUR) AS window,
            COUNT(*) AS count 
        FROM connect 
        GROUP BY name, value, window
    ) AS grouped_bids
) AS ranked_bids 
    
"""