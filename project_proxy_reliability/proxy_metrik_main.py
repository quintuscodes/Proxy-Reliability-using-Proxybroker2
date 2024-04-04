"""Find and show 10 working SOCKS5 proxies and perform a TCP Handshake individually."""

from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.inet import TCP
import asyncio
from proxybroker import Broker
from api import *



def main():
    
    proxies = asyncio.Queue()
    
    broker = Broker(proxies)
    proxy_list= []
    input_proxy_number = int(input('How many proxys should be gathered?\n'))
    input_handshake_tries = int(input('How many handshakes should be established?\n'))
    init_proxy_list(input_proxy_number, proxy_list)
    print_proxy_list_dict(proxy_list)
    
    #list_of_functions = [broker.find(types=[ 'SOCKS5'], limit=10, lvl = 'HIGH', strict = True), 
    #                    write_proxy_to_dict(proxies, proxy_list),broker.show_stats()]
    
    tasks = asyncio.gather(broker.find( types=[ 'SOCKS5'],lvl = 'HIGH', strict = True,limit=input_proxy_number),
                            write_proxy_to_dict(input_proxy_number,proxies, proxy_list,input_handshake_tries),
    )
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)

    counter = 0
    handshake_call(proxy_list, counter,input_handshake_tries)

    balance_proxy_list(proxy_list)
        
    

if __name__ == '__main__':
    main()