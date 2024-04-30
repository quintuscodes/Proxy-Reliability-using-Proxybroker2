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
    input_handshake_tries = 0

    while input_proxy_number < 1: 
        input_proxy_number = int(input('How many proxys >= 10 should be gathered? At least 10 for a realiable list configuration!\n'))
    
    while input_handshake_tries < 2:
        input_handshake_tries = int(input('How many handshakes >= 6 should be established? At least 6 for a realiable list configuration.\n'))
    

    #loop = asyncio.get_event_loop()

    try:

        await socks.fetch_proxys_write_to_class(input_proxy_number,input_handshake_tries,data_size)
        #loop.create_task(http.fetch_proxys_write_to_class(input_proxy_number,input_handshake_tries,data_size))
        # loop.create_task(socks.evaluate_proxy_list(counter, input_handshake_tries,data_size))
        
        #loop.run_forever()
    

    except KeyboardInterrupt:
        #loop.stop()
        pass

    finally: 
        print("Closing Loop")
        
        
        
        
    """
    await asyncio.create_task(socks.fetch_proxys_write_to_class(input_proxy_number,input_handshake_tries,data_size))
    await asyncio.create_task(socks.evaluate_proxy_list(counter,input_handshake_tries,data_size))                 
    
    """
    
    
    
    
    
    
    #http.perform_request()
    
    """
    

    sort_proxy_list(proxy_list)
    refresh_proxy_list(Ready_for_connection,proxy_list,proxy_list_slave)
        
    #requests methode für WEbanfrage mit Proxy
    #request(proxy_list)
    """

if __name__ == '__main__':
   asyncio.run(main())