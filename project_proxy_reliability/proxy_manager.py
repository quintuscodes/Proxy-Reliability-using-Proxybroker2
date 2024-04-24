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
  async def write_proxy_to_class(self,_type, input_number, proxies,input_handshake_tries):
        proxycount = 0
        while True:
            proxy = await proxies.get()
            if proxy is None:
                break
            
            ip = proxy.host
            port = proxy.port
            type = _type
            self.protocol = _type
            p = Proxy(type,ip,port,input_handshake_tries)
            p.add_to_list(self.proxy_list)

  def fetch_proxys_write_to_class(self,input_proxy_number,input_handshake_tries,data_size):
    
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(broker.find( types=[ f'{self.protocol}'],lvl = 'HIGH', strict = True,limit=input_proxy_number),
                            self.write_proxy_to_class(f'{self.protocol}',input_proxy_number, proxies,input_handshake_tries))
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)
    self.print_proxy_list_dict()
    

  def print_proxy_list_dict(self):
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

  def evaluate_proxy_list(self,counter, input_handshake_tries,data_size):
    """
    A Method to initialize the evaluation of the Proxys in Proxy-List
    
    """
    while counter < input_handshake_tries: 
      counter += 1 
      for elements in self.proxy_list:
          index = self.proxy_list.index(elements)
          index += 1
          targetip =  elements.get_ip()
          targetport = elements.get_port()
          
          #create async master_evaluate tasks for one proxy object each,so that all proxys start to be evaluated at once.
          
          elements.master_evaluate(index)
      
      #calc_score(proxy_list,input_handshake_tries)  
      #print_proxy_list_dict(proxy_list) 

      """
      for proxy in proxy_list:
        async create task(proxy.master_evaluate)
      """

