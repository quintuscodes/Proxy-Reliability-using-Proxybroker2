from scapy.all import *
import asyncio
import click
from proxy_class import *
from proxy_manager import *
from functions import *

HTTP_PROTOS = {'HTTP', 'CONNECT:25', 'SOCKS4', 'SOCKS5'}
global proxy_managers_list
global unbalanced
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
    
    

    """
    fetch_tasks = [] 
    evaluate_tasks = []
    refresh_tasks = []   
    proxy_managers_list = []
    

    "Filter by selected protocol and init the tasks"
    counter = 0
    if "HTTP" in protocols:
        http = Proxy_Manager("HTTP") # type: ignore
        proxy_managers_list.append(http)
        fetch_tasks.append(http.fetch_proxys_write_to_class(proxy_number,evaluation_rounds))
        evaluate_tasks.append(http.evaluate_proxy_list(counter, evaluation_rounds,proxy_number))
        refresh_tasks.append(http.refresh_proxy_list(counter,proxy_number,evaluation_rounds ))
    if "SOCKS4" in protocols:
        socks4 = Proxy_Manager("SOCKS4")
        proxy_managers_list.append(socks4)
        fetch_tasks.append(socks4.fetch_proxys_write_to_class(proxy_number,evaluation_rounds))
        evaluate_tasks.append(socks4.evaluate_proxy_list(counter, evaluation_rounds,proxy_number))
        refresh_tasks.append(socks4.refresh_proxy_list(counter,proxy_number,evaluation_rounds ))
    if "SOCKS5" in protocols:
        socks5 = Proxy_Manager("SOCKS5")
        proxy_managers_list.append(socks5)
        fetch_tasks.append(socks5.fetch_proxys_write_to_class(proxy_number,evaluation_rounds))
        evaluate_tasks.append(socks5.evaluate_proxy_list(counter, evaluation_rounds,proxy_number))
        refresh_tasks.append(socks5.refresh_proxy_list(counter,proxy_number,evaluation_rounds ))
    if "CONNECT:25" in protocols:
        connect25 = Proxy_Manager("CONNECT:25")
        proxy_managers_list.append(connect25)
        fetch_tasks.append(connect25.fetch_proxys_write_to_class(proxy_number,evaluation_rounds))
        evaluate_tasks.append(connect25.evaluate_proxy_list(counter, evaluation_rounds,proxy_number))
        refresh_tasks.append(connect25.refresh_proxy_list(counter,proxy_number,evaluation_rounds ))

    num_proto = len(fetch_tasks)
    
    
    "Using Asyncio to concurrently find Proxy Objects using Proxybroker2 and evaluate them using the proxy_class methods "
    
    await asyncio.gather(*fetch_tasks)
    
    await asyncio.gather(*evaluate_tasks)
    
    await sort_proxy_managers(proxy_managers_list,proxy_number) #Sort, Remove not reliable Proxys

        
    "Recursive Re-Evaluate List: Dynamic Approach"
    await rec_wait_and_evaluate_again(proxy_managers_list,counter,evaluation_rounds,proxy_number,num_proto)
    
    


        
        




if __name__ == '__main__':
    run()