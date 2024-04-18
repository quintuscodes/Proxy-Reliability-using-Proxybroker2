"""Find and show 10 working SOCKS5 proxies and perform a TCP Handshake individually."""
from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.inet import TCP
import asyncio
from api import *
from proxy_class import *
from proxy_manager import *



def main():
    Ready_for_connection = False
    proxies = asyncio.Queue()
    
    broker = Broker(proxies)
    global proxy_list 
    proxy_list = []
    proxy_list_slave = []
    socks = Proxy_Manager("SOCKS5")
    http = Proxy_Manager("HTTP")
    https = Proxy_Manager("SOCKS4")
    




    
    input_proxy_number = 0




    
    while input_proxy_number < 1: 
        input_proxy_number = int(input('How many proxys >= 10 should be gathered? At least 10 for a realiable list configuration!\n'))
    
    input_handshake_tries = 0

    while input_handshake_tries < 2:
        input_handshake_tries = int(input('How many handshakes >= 6 should be established? At least 6 for a realiable list configuration.\n'))
    
    data_size =1000
    
    socks.fetch_proxys_write_to_class(input_proxy_number,input_handshake_tries,data_size)
    http.fetch_proxys_write_to_class(input_proxy_number,input_handshake_tries,data_size)
    https.fetch_proxys_write_to_class(input_proxy_number,input_handshake_tries,data_size)

    """
    #init_proxy_list(input_proxy_number, proxy_list)
    #print_proxy_list_dict(proxy_list)
    
    #list_of_functions = [broker.find(types=[ 'SOCKS5'], limit=10, lvl = 'HIGH', strict = True), 
    #                    write_proxy_to_dict(proxies, proxy_list),broker.show_stats()]
    
    tasks = asyncio.gather(broker.find( types=[ 'SOCKS5'],lvl = 'HIGH', strict = True,limit=input_proxy_number),
                            s.write_proxy_to_class('SOCKS5',input_proxy_number, proxies,input_handshake_tries),
    )
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)
    print_proxy_list_dict(s.proxy_list)
    
    counter = 0
    evaluate_call(proxy_list, counter,input_handshake_tries,data_size)

    sort_proxy_list(proxy_list)
    refresh_proxy_list(Ready_for_connection,proxy_list,proxy_list_slave)
        
    #requests methode für WEbanfrage mit Proxy
    #request(proxy_list)
    """
if __name__ == '__main__':
    main()