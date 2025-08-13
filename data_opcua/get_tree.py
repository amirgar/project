import asyncio
from asyncua import Node, ua
from asyncua.client import Client
from asyncua.client.ua_file import UaFile
from pprint import pprint
import yaml


async def rec(client: Client, cur_nod, way = []) -> dict: 
    cur = {}
    if await cur_nod.get_children():
        for child in await cur_nod.get_children():
            way.append(f'2:{(await child.read_display_name()).Text}')
            cur[(await child.read_display_name()).Text] = await rec(client, child, way)
            way.pop()
    try:
        root = client.get_objects_node()
        if not await (await root.get_child(way)).get_children():
            try:
                curvar = await (await root.get_child(way)).read_browse_name()
                # print(await curvar.read_browse_name())
                return {curvar: "null"}
            except Exception as e: 
                pass
    except: 
        pass
    finally: 
        return cur


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
        root = client.get_root_node()
        children = await root.get_children()
        for child in children: 
            print(child)
        tree = await rec(client, root)
        with open("tree2.yaml", "w") as file:
            yaml.dump(tree, file)


if __name__ == "__main__":
    asyncio.run(main())
