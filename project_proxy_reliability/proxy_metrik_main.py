
from scapy.all import *
import asyncio
import click
from proxy_class import *
from proxy_manager import *


HTTP_PROTOS = {'HTTP', 'CONNECT:25', 'SOCKS4', 'SOCKS5'}

@click.command()
@click.argument("proxy_number",type=int)
@click.argument("evaluation_rounds", type=int)
@click.option('--protocols', default = 'HTTP',prompt='Enter the Protocols{HTTP,CONNECT:25, SOCKS4,SOCKS5} to be gathered',help='Enter the Protocols{"HTTP" "CONNECT:25", "SOCKS4", "SOCKS5"} to be gathered separated by a comma like HTTP,SOCKS4,CONNECT25')
def run(proxy_number: int, evaluation_rounds: int, protocols: set):
    """
    CLI command to start the proxy evaluation with specified number of proxies and evaluation rounds wrapped in an Asyncio Event Loop to find and evaluate Proxys concurrently
    
    TODO: Code fuer CLI um protokolle per click.option anzugeben. fetch,evaluate, refresh tasks und abfrage aus main anpassen.
    
    """
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(proxy_number, evaluation_rounds, protocols))
    

async def main(proxy_number: int,evaluation_rounds:int, protocols: set):
    
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
    
    
    
    "Using Asyncio to concurrently find Proxy Objects using Proxybroker2 and evaluate them using the proxy_class methods "
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
        checked = []
        for items in proxy_managers_list:
            
            if len(items.master_proxy_list) == proxy_number:
                checked.append(1)

        if checked.count(1) == num_proto:
              print("CHECK approved")
              await asyncio.sleep(5)

              unbalanced = False
              end_time = time.perf_counter()
              evaluation_time = end_time - start_time
              num_proto = len(fetch_tasks)

              await print_proxy_managers(proxy_managers_list,master)
              print("\n\n      ------- Initiated Termination -------\n\n     ^                                         ^\n     |   Here is the final Master Proxy List   |\n")
              print(f"Die Evaluation von {proxy_number} Proxys bei {input_evaluation_rounds} Evaluationsrunden und {num_proto}  Protokollen dauerte {evaluation_time} s \n")
        else:
            print("Notdoneyet")
            await asyncio.sleep(5)

    await wait_and_evaluate_loop()


async def print_proxy_managers(list,arg):
    for proxy_manager_item in list:
        await proxy_manager_item.print_proxy_list(arg)

async def sort_proxy_managers(list,proxy_number):
    for proxy_manager_item in list:
        await proxy_manager_item.sort_proxy_lists(proxy_number)

async def wait_and_evaluate_loop():
    print("Wait 30s until Master List re-evaluate.\n")
    for _ in range(15):  # 40 Sekunden / 2 Sekunden = 20
        await asyncio.sleep(2)
        print('.', end='',flush=True)
    print('\nEvaluate Master List again!')


if __name__ == '__main__':
    run()