"""Find and show 10 working SOCKS5 proxies and perform a TCP Handshake individually."""
from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.inet import TCP
import asyncio
import click
from proxy_class import *
from proxy_manager import *



async def main():
    
    Ready_for_connection = False
    data_size =1000
    
    
    """
    HTTP, SOCKS4, SOCKS5, CONNECT:25 
    """
    http = Proxy_Manager("HTTP")
    #socks4 = Proxy_Manager("SOCKS4")
    socks5 = Proxy_Manager("SOCKS5")
    #connect25 = Proxy_Manager("CONNECT:25")

    counter = 0
    input_proxy_number = 0
    input_evaluation_rounds = 0
    
    while input_proxy_number < 1: 
        input_proxy_number = int(input('How many proxys >= 10 should be gathered? At least 10 for a realiable list configuration!\n'))
    
    while input_evaluation_rounds < 1:
        input_evaluation_rounds = int(input('How many handshakes >= 6 should be established? At least 6 for a reliable list configuration.\n'))
    """
    start_time = time.perf_counter()
    await socks.fetch_proxys_write_to_class(input_proxy_number,input_evaluation_rounds,data_size)
    await http.fetch_proxys_write_to_class(input_proxy_number,input_evaluation_rounds,data_size)
    
    await socks.evaluate_proxy_list(counter, input_evaluation_rounds,data_size, input_proxy_number)
    await http.evaluate_proxy_list(counter, input_evaluation_rounds,data_size, input_proxy_number)
    end_time = time.perf_counter()
    await socks.print_proxy_list()
    await http.print_proxy_list()
    evaluation_time = end_time - start_time
    
    """
    start_time = time.perf_counter()
    fetch_tasks = [socks5.fetch_proxys_write_to_class(input_proxy_number,input_evaluation_rounds,data_size),
                   http.fetch_proxys_write_to_class(input_proxy_number,input_evaluation_rounds,data_size),
                   ] 
    evaluate_tasks = [socks5.evaluate_proxy_list(counter, input_evaluation_rounds,data_size, input_proxy_number),
                      http.evaluate_proxy_list(counter, input_evaluation_rounds,data_size, input_proxy_number),
                      ]   

    await asyncio.gather(*fetch_tasks)
    await asyncio.gather(*evaluate_tasks)
    end_time = time.perf_counter()

    
    await socks5.print_proxy_list()
    await http.print_proxy_list()
    

    evaluation_time = end_time - start_time
    num_proto = len(fetch_tasks)
    print(f"Die Evaluation von {input_proxy_number} Proxys bei {input_evaluation_rounds} Evaluationsrunden und {num_proto}  Protokollen dauerte {evaluation_time} s ")
    
    await socks5.sort_proxy_list()
    await http.sort_proxy_list()

    await socks5.print_proxy_list()
    await http.print_proxy_list()

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