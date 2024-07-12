
from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.inet import TCP
import asyncio
import click
from proxy_class import *
from proxy_manager import *



@click.command()
@click.argument("proxy_number",type=int)
@click.argument("evaluation_rounds", type=int)

#@click.option('--proxy', default=10, prompt='Enter the Number of reliable Proxy-Servers to be gathered for each protocol.', help='Number of reliable Proxy-Servers to be gathered for each protocol.')
#@click.option('--evaluation_rounds', default=4,prompt='Enter the Number of Evaluation Rounds. ',
#             help='Number of Rounds Handshake, Request, Transmission Time, Throughput should be evaluated. The greater the number of rounds, the more precise the proxy evaluation. ')
def run(proxy_number: int, evaluation_rounds: int):
    """
    CLI command to start the proxy evaluation with specified number of proxies and evaluation rounds wrapped in an Asyncio Event Loop to find and evaluate Proxys concurrently
    """
    ""
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(proxy_number, evaluation_rounds))
    

async def main(proxy_number: int,evaluation_rounds:int):
    
    """

    Asynchronous Main Funtion to instantiate Proxy-Manager Object for a specific Protocol, find, evaluate and generate a dynamic list with reliable Proxys given a score.


    HTTP, SOCKS4, SOCKS5, CONNECT:25 
    
    Comment out/in desired Protocols

        """

    http = Proxy_Manager("HTTP")
    socks4 = Proxy_Manager("SOCKS4")
    socks5 = Proxy_Manager("SOCKS5")
    connect25 = Proxy_Manager("CONNECT:25")

    proxy_managers_list = []
    proxy_managers_list.append(http)
    proxy_managers_list.append(socks4)
    proxy_managers_list.append(socks5)
    proxy_managers_list.append(connect25)

    
    data_size =1000
    master = "master"
    global unbalanced
    unbalanced = True
    counter = 0
    input_evaluation_rounds = evaluation_rounds
    
    start_time = time.perf_counter()

    "Remove/Add here desired protocols"
    fetch_tasks = [socks5.fetch_proxys_write_to_class(proxy_number,input_evaluation_rounds,data_size),
                   http.fetch_proxys_write_to_class(proxy_number,input_evaluation_rounds,data_size),
                   socks4.fetch_proxys_write_to_class(proxy_number,input_evaluation_rounds,data_size),
                   connect25.fetch_proxys_write_to_class(proxy_number,input_evaluation_rounds,data_size)
                   ] 
    evaluate_tasks = [socks5.evaluate_proxy_list(counter, input_evaluation_rounds,data_size, proxy_number),
                      http.evaluate_proxy_list(counter, input_evaluation_rounds,data_size, proxy_number),
                      socks4.evaluate_proxy_list(counter, input_evaluation_rounds,data_size, proxy_number),
                      connect25.evaluate_proxy_list(counter, input_evaluation_rounds,data_size, proxy_number)
                      ]   
    
    
    
    
    await asyncio.gather(*fetch_tasks)
    await asyncio.gather(*evaluate_tasks)
    end_time = time.perf_counter()

    
    
    evaluation_time = end_time - start_time
    num_proto = len(fetch_tasks)
    print(f"Die Evaluation von {proxy_number} Proxys bei {input_evaluation_rounds} Evaluationsrunden und {num_proto}  Protokollen dauerte {evaluation_time} s ")
    
    await sort_proxy_managers(proxy_managers_list,proxy_number)

    
    "Checker-Method"
    while unbalanced:

        await asyncio.sleep(5)
        print("CHECKER METHOD active\n")
        
        await print_proxy_managers(proxy_managers_list,0)
        
        await print_proxy_managers(proxy_managers_list,master)
        await asyncio.sleep(5)

        
        
        print(f"Query new reliable Proxys to MASTER List ")

        "Remove/Add here desired protocols"
        refresh_tasks = [socks5.refresh_proxy_list(counter,proxy_number,input_evaluation_rounds,data_size ),
                     http.refresh_proxy_list(counter,proxy_number,input_evaluation_rounds,data_size ),
                     socks4.refresh_proxy_list(counter,proxy_number,input_evaluation_rounds,data_size ),
                     connect25.refresh_proxy_list(counter,proxy_number,input_evaluation_rounds,data_size )
                     ]
        await asyncio.gather(*refresh_tasks)
        
        "Remove/Add here desired protocols in if - statement"
        if len(http.master_proxy_list) == proxy_number and len(socks5.master_proxy_list) == proxy_number and len(socks4.master_proxy_list) == proxy_number and len(connect25.master_proxy_list) == proxy_number:
              unbalanced = False
              end_time = time.perf_counter()
              evaluation_time = end_time - start_time
              num_proto = len(fetch_tasks)

              await print_proxy_managers(proxy_managers_list,master)
              print("\n\n      ------- Initiated Termination -------\n\n     ^                                         ^\n     |   Here is the final Master Proxy List   |\n")
              print(f"Die Evaluation von {proxy_number} Proxys bei {input_evaluation_rounds} Evaluationsrunden und {num_proto}  Protokollen dauerte {evaluation_time} s ")
    

        query = int(input("Enter 1 to continue and 0 to cancel\n")) # For Future Events 
        if query == 1:
            print("\n\n Continue \n")
        else:
           unbalanced = False

           await print_proxy_managers(proxy_managers_list,master)
           print("\n\n      ------- Initiated Termination -------\n\n     ^                                         ^\n     |   Here is the final Master Proxy List   |\n")

async def print_proxy_managers(list,arg):
    for proxy_manager_item in list:
        await proxy_manager_item.print_proxy_list(arg)

async def sort_proxy_managers(list,proxy_number):
    for proxy_manager_item in list:
        await proxy_manager_item.sort_proxy_lists(proxy_number)



if __name__ == '__main__':
    run()