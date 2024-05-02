"""
A Class for managing Proxy Evaluation and performing Request. This is the target data structure.

"""
from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.inet import TCP
import asyncio
from proxybroker import Broker, Proxy
from proxy_class import *
from proxy_manager import *

#import requests

class Proxy_Manager:
  """
  A Class for Managing Proxy List and Evaluation
  """
  def __init__(self,_protocol):
    self.protocol = _protocol
    self.master_proxy_list = []
    self.proxy_list = []
  
  

  def get_proxy(self, index) -> Proxy:
     proxy = self.proxy_list[index]
     
     return proxy
  """
  def perform_request(self):
    "Perform the Request with [1] in master list"
    
       
    proxies = {
       f"{self.protocol.lower()}": f"{self.proxy_list[0].get_ip()}:{self.proxy_list[0].get_port()}",
       f"{self.protocol.lower()}": f"{self.proxy_list[1].get_ip()}:{self.proxy_list[1].get_port()}"

    }
  
    response = requests.get("https://httpbin.org/get", proxies=proxies)
    print(response.text)
  """

  async def write_proxy_to_class(self,_type, input_number, proxies,input_evaluation_rounds):
        proxycount = 0
        while True:
            proxy = await proxies.get()
            if proxy is None:
                break
            
            ip = proxy.host
            port = proxy.port
            type = _type
            self.protocol = _type
            p = Proxy(type,ip,port,input_evaluation_rounds)
            p.add_to_list(self.proxy_list)

  async def fetch_proxys_write_to_class(self,input_proxy_number,input_evaluation_rounds,data_size):
    
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    print("test")
    await broker.find( types=[ f'{self.protocol}'],lvl = 'HIGH', strict = True,limit=input_proxy_number)
    await self.write_proxy_to_class(f'{self.protocol}',input_proxy_number, proxies,input_evaluation_rounds)
    
    await self.print_proxy_list()
    





  async def print_proxy_list(self):
    """
    A function to print the actual proxy_list
    """
    
    
    print("\n \n ")
    print(f"{self.protocol} Proxy - Manager")
    print(" ____________________________________________________________________________________________________________________________________________________________________")
    print("|\n \n")
    print("   Proxy - Liste")
    print("   __________________________________________________________________________________________________________________________________________________________________")
    print("  |\n")
    for elements in self.proxy_list:
        index = self.proxy_list.index(elements)
        index += 1
        attrs = vars(elements)
        print(f"      > {index}. Proxy \n \n      " + ', \n      '.join("%s: %s" % item for item in attrs.items()) + "\n")
        #print(f', \n'.join("%s: %s" % item for item in attrs.items()) + "\n")
    print("  |__________________________________________________________________________________________________________________________________________________________________\n \n \n")
    print("|_____________________________________________________________________________________________________________________________________________________________________")
    print("\n \n") 

  async def evaluate_proxy_list(self,counter, input_evaluation_rounds,data_size, input_proxy_number):
    """
    A Method to initialize the evaluation of the Proxys in Proxy-List
    
    """
    
    
    
    while counter < input_evaluation_rounds: 
      counter += 1 
      
      queue = asyncio.Queue(maxsize=input_proxy_number)
      """
      What exactly needs to be added to the queue?
      """
      tasks = []
      
      for i in range(self.proxy_list.len()):
          index = self.proxy_list.index(i)

          proxy = self.get_proxy(i)

          index += 1
          
          task1 = asyncio.create_task(proxy.evaluate_handshakes(queue))
          task2 = asyncio.create_task(proxy.evaluate_transmission_time(queue))
          task3 = asyncio.create_task(proxy.evaluate_throughput(queue))

          tasks.append(task1)
          tasks.append(task2)
          tasks.append(task3)

          #create async master_evaluate tasks for one proxy object each,so that all proxys start to be evaluated at once.
          
          #for each proxy create_task(proxy.master_evaluate())
          
      await queue.join() 

      for task in tasks:
        task.cancel()
        # Wait until all worker tasks are cancelled.
      
      await asyncio.gather(*tasks, return_exceptions=True)

      



    #calc_score(proxy_list,input_evaluation_rounds)  
    #print_proxy_list_dict(proxy_list) 

    """
    for proxy in proxy_list:
      async create task(proxy.master_evaluate)
    """

