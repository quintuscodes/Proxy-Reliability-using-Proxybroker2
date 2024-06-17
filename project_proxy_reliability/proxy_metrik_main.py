"""Find and show 10 working SOCKS5 proxies and perform a TCP Handshake individually."""
from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.inet import TCP
import asyncio

from proxy_class import *
from proxy_manager import *



async def main():
    
    Ready_for_connection = False
    data_size =1000
    proxy_list_slave = []

    socks = Proxy_Manager("SOCKS5")
    http = Proxy_Manager("HTTP")
    
    counter = 0
    input_proxy_number = 0
    input_evaluation_rounds = 0

    while input_proxy_number < 1: 
        input_proxy_number = int(input('How many proxys >= 10 should be gathered? At least 10 for a realiable list configuration!\n'))
    
    while input_evaluation_rounds < 1:
        input_evaluation_rounds = int(input('How many handshakes >= 6 should be established? At least 6 for a realiable list configuration.\n'))
    
    #TODO Set up two event loops one for gathering proxys, one for doing the evaluation

    await socks.fetch_proxys_write_to_class(input_proxy_number,input_evaluation_rounds,data_size)
    await socks.evaluate_proxy_list(counter, input_evaluation_rounds,data_size, input_proxy_number)
    
    
        
        
"""
    #http.perform_request()
    sort_proxy_list(proxy_list)
    refresh_proxy_list(Ready_for_connection,proxy_list,proxy_list_slave)
        
    #requests methode für WEbanfrage mit Proxy
    #request(proxy_list)
"""

if __name__ == '__main__':
   loop = asyncio.get_event_loop()
   loop.run_until_complete(main())