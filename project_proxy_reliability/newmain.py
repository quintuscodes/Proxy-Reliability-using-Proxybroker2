from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.inet import TCP
import asyncio

from proxy_class import *
from proxy_manager import *


async def worker(num):
    print("running: ",num)
    await asyncio.sleep(1)
    print("Finished: ", num)

async def main():
    """
    data_size =1000
    socks = Proxy_Manager("SOCKS5")

    input_proxy_number = 0
    input_evaluation_rounds = 0

    while input_proxy_number < 1: 
        input_proxy_number = int(input('How many proxys >= 10 should be gathered? At least 10 for a realiable list configuration!\n'))
    
    while input_evaluation_rounds < 2:
        input_evaluation_rounds = int(input('How many handshakes >= 6 should be established? At least 6 for a realiable list configuration.\n'))
    """
    print("Started")
    tasklist = []

    for i in range(1,40 + 1):
        tasklist.append(worker(i))

    await asyncio.sleep(2)
    await asyncio.gather(*tasklist)
    
    print("Done!")

if __name__  == '__main__':
    asyncio.run(main())

