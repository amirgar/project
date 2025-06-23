from asyncua import Client
import asyncio

async def print_devices():
    async with Client(url='opc.tcp://administrator@10.0.2.22:4840/') as client:
        while True:
            # Do something with client
            node = client.get_node('i=15')
            value = await node.read_value()

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_devices())
    loop.close()

if __name__ == '__main__':
    main()