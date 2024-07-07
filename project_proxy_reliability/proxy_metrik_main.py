
from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.inet import TCP
import asyncio
import click
from proxy_class import *
from proxy_manager import *



async def main():
    
    """

    Asynchronous Main Funtion to instantiate Proxy-Manager Object for a specific Protocol, find, evaluate and store reliable Proxys given a score


    HTTP, SOCKS4, SOCKS5, CONNECT:25 
    - Need to adapt main() with fetch_, print() &  evaluate_ tasks to gather other protocols if desired

    """

    http = Proxy_Manager("HTTP")
    socks4 = Proxy_Manager("SOCKS4")
    socks5 = Proxy_Manager("SOCKS5")
    connect25 = Proxy_Manager("CONNECT:25")

    proxy_managers_list = []
    proxy_managers_list.append(http,socks4,socks5,connect25)

    data_size =1000
    master = "master"
    global unbalanced
    unbalanced = True
    counter = 0
    input_proxy_number = 0
    input_evaluation_rounds = 0
    
    while input_proxy_number < 1: 
        input_proxy_number = int(input('How many proxys >= 10 should be gathered? At least 10 for a realiable list configuration!\n'))
    
    while input_evaluation_rounds < 1:
        input_evaluation_rounds = int(input('How many handshakes >= 6 should be established? At least 6 for a reliable list configuration.\n'))
    
    start_time = time.perf_counter()

    "Add here different protocols"
    fetch_tasks = [socks5.fetch_proxys_write_to_class(input_proxy_number,input_evaluation_rounds,data_size),
                   http.fetch_proxys_write_to_class(input_proxy_number,input_evaluation_rounds,data_size),
                   socks4.fetch_proxys_write_to_class(input_proxy_number,input_evaluation_rounds,data_size),
                   connect25.fetch_proxys_write_to_class(input_proxy_number,input_evaluation_rounds,data_size)
                   ] 
    evaluate_tasks = [socks5.evaluate_proxy_list(counter, input_evaluation_rounds,data_size, input_proxy_number),
                      http.evaluate_proxy_list(counter, input_evaluation_rounds,data_size, input_proxy_number),
                      socks4.evaluate_proxy_list(counter, input_evaluation_rounds,data_size, input_proxy_number),
                      connect25.evaluate_proxy_list(counter, input_evaluation_rounds,data_size, input_proxy_number)
                      ]   
    
    
    
    
    await asyncio.gather(*fetch_tasks)
    await asyncio.gather(*evaluate_tasks)
    end_time = time.perf_counter()

    
    
    evaluation_time = end_time - start_time
    num_proto = len(fetch_tasks)
    print(f"Die Evaluation von {input_proxy_number} Proxys bei {input_evaluation_rounds} Evaluationsrunden und {num_proto}  Protokollen dauerte {evaluation_time} s ")
    
    await socks5.sort_proxy_lists()
    await http.sort_proxy_lists()
    await socks4.sort_proxy_lists()
    await connect25.sort_proxy_lists()

    
    "Checker-Method"
    while unbalanced:

        await asyncio.sleep(5)
        print("CHECKER METHOD active\n")
        await socks5.print_proxy_list(0)
        await http.print_proxy_list(0)
        await socks4.print_proxy_list(0)
        await connect25.print_proxy_list(0)
        await socks5.print_proxy_list(master)
        await http.print_proxy_list(master)
        await socks4.print_proxy_list(master)
        await connect25.print_proxy_list(master)

        await asyncio.sleep(5)

        
        
        print(f"Query new reliable Proxys to MASTER List ")

        refresh_tasks = [socks5.refresh_proxy_list(counter,input_proxy_number,input_evaluation_rounds,data_size ),
                     http.refresh_proxy_list(counter,input_proxy_number,input_evaluation_rounds,data_size ),
                     socks4.refresh_proxy_list(counter,input_proxy_number,input_evaluation_rounds,data_size ),
                     connect25.refresh_proxy_list(counter,input_proxy_number,input_evaluation_rounds,data_size )
                     ]
        await asyncio.gather(*refresh_tasks)
        
          
        if len(http.master_proxy_list) == 10 and len(socks5.master_proxy_list) == 10 and len(socks4.master_proxy_list) == 10 and len(connect25.master_proxy_list) == 10:
              unbalanced = False
              print("\n\n      ------- Initiated Termination -------\n       Here is the final Master Proxy List\n")
              await socks5.print_proxy_list(master)
              await http.print_proxy_list(master)
              await socks4.print_proxy_list(master)
              await connect25.print_proxy_list(master)

        query = int(input("Enter 1 to continue and 0 to abort\n"))
        if query == 1:
            print("\n\n Continue \n")
        else:
           unbalanced = False
           print("\n\n      ------- Initiated Termination -------\n       Here is the final Master Proxy List\n")
           await socks5.print_proxy_list(master)
           await http.print_proxy_list(master)
           await socks4.print_proxy_list(master)
           await connect25.print_proxy_list(master)
   

async def print_proxy_managers(list,arg):
    for proxy_manager in list:
        await proxy_manager.print_proxy_list(arg)



if __name__ == '__main__':
    "Asyncio Event Loop to find and evaluate Proxys concurrently"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())