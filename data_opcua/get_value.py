import asyncio
from asyncua import Node, ua
from asyncua.client import Client
from asyncua.client.ua_file import UaFile
from pprint import pprint
from datetime import datetime
import aiokafka
import json
import yaml


ans = []


async def rec(client: Client, cur_nod):
    global ans
    if len(ans) >= 30: 
        return
    if await cur_nod.get_children():
        for child in await cur_nod.get_children():
            # Проверяем, есть ли у дочернего узла потомки
            if not await child.get_children():
                try:
                    # print(await child.read_browse_name(), await child.read_value())
                    ans.append(f"{await child.read_browse_name()}: {await child.read_value()}")
                except Exception:
                    # print(await child.read_browse_name(), "None")
                    ans.append(f"{await child.read_browse_name()}: None")
            else:
                await rec(client, child)


def convert(s: str) -> list: 
    i = s[3]
    s = s.split(".")
    s[0] = s[0][7:]
    res = [f'{i}:{el}' for el in s]
    return res 


async def main():
    url = "opc.tcp://MrSmith:Doosan040100000*@10.194.2.38:49320"
    async with Client(url=url) as client:
        await client.connect()
        await client.load_data_type_definitions()
        root = await client.get_objects_node().get_child(convert("ns=2;i=401000016_AVZ_SW800_OPC_DPA.Device1.Alias.Alarm"))
        print(root)
        print(await root.read_value())
        await asyncio.sleep(2)
        print(await root.read_value())
        for child in await root.get_children():
            try:
                print(await child.read_browse_name(), await child.read_value())
            except Exception:
                print(await child.read_browse_name(), "None")
        await asyncio.sleep(1)
        for child in await root.get_children():
            try:
                print(await child.read_browse_name(), await child.read_value())
            except Exception:
                print(await child.read_browse_name(), "None")


if __name__ == "__main__":
    asyncio.run(main())
