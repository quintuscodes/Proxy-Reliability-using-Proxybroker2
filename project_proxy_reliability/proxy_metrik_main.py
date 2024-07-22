
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

    fetch_tasks = [] 
    evaluate_tasks = []
    refresh_tasks = []   
    proxy_managers_list = []

    data_size =1000
    master = "master"
    global unbalanced
    unbalanced = True
    counter = 0
    input_evaluation_rounds = evaluation_rounds

    
    if "HTTP" in protocols:
        proxy_managers_list.append(http)
        fetch_tasks.append(http.fetch_proxys_write_to_class(proxy_number,input_evaluation_rounds,data_size))
        evaluate_tasks.append(http.evaluate_proxy_list(counter, input_evaluation_rounds,data_size, proxy_number))
        refresh_tasks.append(http.refresh_proxy_list(counter,proxy_number,input_evaluation_rounds,data_size ))
    if "SOCKS4" in protocols:
        proxy_managers_list.append(socks4)
        fetch_tasks.append(socks4.fetch_proxys_write_to_class(proxy_number,input_evaluation_rounds,data_size))
        evaluate_tasks.append(socks4.evaluate_proxy_list(counter, input_evaluation_rounds,data_size, proxy_number))
        refresh_tasks.append(socks4.refresh_proxy_list(counter,proxy_number,input_evaluation_rounds,data_size ))
    if "SOCKS5" in protocols:
        proxy_managers_list.append(socks5)
        fetch_tasks.append(socks5.fetch_proxys_write_to_class(proxy_number,input_evaluation_rounds,data_size))
        evaluate_tasks.append(socks5.evaluate_proxy_list(counter, input_evaluation_rounds,data_size, proxy_number))
        refresh_tasks.append(socks5.refresh_proxy_list(counter,proxy_number,input_evaluation_rounds,data_size ))
    if "CONNECT:25" in protocols:   
        proxy_managers_list.append(connect25)
        fetch_tasks.append(connect25.fetch_proxys_write_to_class(proxy_number,input_evaluation_rounds,data_size))
        evaluate_tasks.append(connect25.evaluate_proxy_list(counter, input_evaluation_rounds,data_size, proxy_number))
        refresh_tasks.append(connect25.refresh_proxy_list(counter,proxy_number,input_evaluation_rounds,data_size ))

    
    
    
    "Using Asyncio to concurrently find Proxy Objects using Proxybroker2 and evaluate them using the proxy_class methods "
    
    await asyncio.gather(*fetch_tasks)
    start_time = time.perf_counter()
    await asyncio.gather(*evaluate_tasks)
    end_time = time.perf_counter()

    
    
    evaluation_time = end_time - start_time
    num_proto = len(fetch_tasks)
    print(f"The Evaluation of {proxy_number} Proxys in {input_evaluation_rounds} Evaluation Rounds of {num_proto}  protocols took {evaluation_time} s ")
    
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

    await rec_wait_and_evaluate_again(proxy_managers_list)
    await print_proxy_managers(proxy_managers_list,master)

async def print_proxy_managers(list,arg):
    for proxy_manager_item in list:
        await proxy_manager_item.print_proxy_list(arg)

async def sort_proxy_managers(list,proxy_number):
    for proxy_manager_item in list:
        await proxy_manager_item.sort_proxy_lists(proxy_number)

async def reset_proxy_objects(list):
    for proxy_manager_item in list:
        await proxy_manager_item.reset_proxys()

async def rec_wait_and_evaluate_again(proxy_managers_list):
    print("Wait 30s until Master List re-evaluate.\n")
    for _ in range(15):  # 40 Sekunden / 2 Sekunden = 20
        await asyncio.sleep(2)
        print('.', end='',flush=True)
    print('\nEvaluate Master List again!\n')

    """The Recursive Loop to Re-Evaluate
    Here goes the Code to 
    > reset proxy.ip and proxy.port in the proxy managers master lists -> TODO: Write a Method to iterate through the Proxy_Manager_lists 
    > evaluate_tasks neu befüllen ->Function 
    > start asyncio.gather(*evaluate_tasks) 
    """
    await reset_proxy_objects(proxy_managers_list)
    
    #await rec_wait_and_evaluate_again(proxy_managers_list)
    



if __name__ == '__main__':
    run()