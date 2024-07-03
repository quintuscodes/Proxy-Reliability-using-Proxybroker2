"""
A Class for managing Proxy Evaluation and performing Request. This is the target data structure.

"""
from scapy.all import *
import queue
import threading
from scapy.layers.inet import IP
from scapy.layers.inet import TCP
import asyncio
import aiohttp
from proxybroker import Broker, Proxy # type: ignore
from proxy_class import *
from proxy_manager import *
from proxy_metrik_main import *

#import requests

class Proxy_Manager:

  """
  A Class for Managing Protocol Proxy List and Evaluation
  """


  "Construcotr"
  def __init__(self,_protocol):
    self.ready_for_connection = False
    self.protocol = _protocol
    self.master_proxy_list = []
    self.proxy_list = []
    self.proxy_list_slave = []
  
  "Helper Method to get proxy items from list"

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

  

  async def fetch_proxys_write_to_class(self,input_proxy_number,input_evaluation_rounds,data_size):
    "Fetching Proxys from open Source using proxybroker2 and writitng them to customized class"

    proxies = asyncio.Queue()
    
   
    broker = Broker(proxies)
    print("test")
    await broker.find( types=[ f'{self.protocol}'],lvl = 'HIGH', strict = True,limit=input_proxy_number)
    await self.write_proxy_to_class(f'{self.protocol}',input_proxy_number, proxies,input_evaluation_rounds)
      
    await self.print_proxy_list(0)
    
  async def write_proxy_to_class(self,_type, input_number, proxies,input_evaluation_rounds):
    "Method to write proxys to customized class and adding to proxy list  "

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
      self.add_to_list(p)

  "Method to add a Proxy item to the list "
  def add_to_list(self,Proxy):
    self.proxy_list.append(Proxy)
    
    attrs = vars(Proxy)
    print(f"\nAdded to List:\n" + ', \n'.join("%s: %s" % item for item in attrs.items()) + "\n")

  async def print_proxy_list(self,arg):
    """
    Method to print the actual proxy_list
    """
    
    if arg == "master":
       
      print("\n \n ")
      print(f"{self.protocol} Proxy - Manager")
      print(" ____________________________________________________________________________________________________________________________________________________________________")
      print("|\n \n")
      print("   **** MASTER **** Proxy - Liste")
      print("   __________________________________________________________________________________________________________________________________________________________________")
      print("  |\n")

      for elements in self.master_proxy_list:
          index = self.master_proxy_list.index(elements)
          index += 1
          attrs = vars(elements)
          print(f"      > {index}. Proxy \n \n      " + ', \n      '.join("%s: %s" % item for item in attrs.items()) + "\n")
         

      print("  |__________________________________________________________________________________________________________________________________________________________________\n \n \n")
      print("|_____________________________________________________________________________________________________________________________________________________________________")
      print("\n \n") 

    else:

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
          

      print("  |__________________________________________________________________________________________________________________________________________________________________\n \n \n")
      print("|_____________________________________________________________________________________________________________________________________________________________________")
      print("\n \n") 

  async def evaluate_proxy_list(self,counter, input_evaluation_rounds,data_size, input_proxy_number):
    
    """
    A Method to initialize the evaluation of the Proxys in Proxy-List
    
    """
    
    
    
    while counter < input_evaluation_rounds: 
      counter += 1 
      
    
      tasks = []
      print(f"Test Queue Evaluation Round Nr. {counter}")
      
      
      for i in range(len(self.proxy_list)):
        proxy = self.get_proxy(i)
        task = proxy.evaluate()             #Evaluate Thread Pool Executor -> Evaluation Methods {handshake,transmission_time,throughput,request}
        tasks.append(task)
        
        

      await asyncio.gather(*tasks)
    
    for i in range(len(self.proxy_list)):
        proxy = self.get_proxy(i)
        proxy.calc_score(input_evaluation_rounds) #loop through proxy_list and calculate score per proxy

    "Reward the Best Proxys in evaluation parameters - sort after score - then give 15,10,5 Points credit score"

    first = 15
    second = 10
    third = 5

    for i in range(3):
      if i == 0:
        self.proxy_list.sort(key=lambda Proxy: Proxy.avg_syn_ack_time, reverse=False) 

      elif i == 1:
        self.proxy_list.sort(key=lambda Proxy: Proxy.avg_transmission_time, reverse=False)

      elif i == 2:
         self.proxy_list.sort(key=lambda Proxy: Proxy.avg_throughput, reverse=True)
      
      if len(self.proxy_list) >= 1:
        self.proxy_list[0].score += first
        if i == 0:
          print(f"{first}  Points Credit to IP: {self.proxy_list[0].ip} in avg_syn_ack_time PROT: {self.protocol}  ")
        if i == 1:
          print(f"{first}  Points Credit to IP: {self.proxy_list[0].ip} in avg_transmission_time PROT: {self.protocol}  ")
        if i == 2:
          print(f"{first}  Points Credit to IP: {self.proxy_list[0].ip} in avg_throughput PROT: {self.protocol}  ")
      
      if len(self.proxy_list) >= 2:
        self.proxy_list[1].score += second
        if i == 0:
          print(f"{second} Points Credit to IP: {self.proxy_list[1].ip} in avg_syn_ack_time PROT: {self.protocol}  ")
        if i == 1:
          print(f"{second} Points Credit to IP: {self.proxy_list[1].ip} in avg_transmission_time PROT: {self.protocol} ")
        if i == 2:
          print(f"{second} Points Credit to IP: {self.proxy_list[1].ip} in avg_throughput PROT: {self.protocol} ")
        
      
      if len(self.proxy_list) >= 3:
        self.proxy_list[2].score += third
        if i == 0:
          print(f"{third} Points Credit to IP: {self.proxy_list[2].ip} in avg_syn_ack_time PROT: {self.protocol} ")
        if i == 1:
          print(f"{third} Points Credit to IP: {self.proxy_list[2].ip} in avg_transmission_time PROT: {self.protocol} ")
        if i == 2:
          print(f"{third} Points Credit to IP: {self.proxy_list[2].ip} in avg_throughput PROT: {self.protocol} ")
        
    
    self.proxy_list.sort(key=lambda Proxy: Proxy.score, reverse=True)
    


  async def sort_proxy_lists(self):
    "A Method to sort the List and remove proxys with a < 100 score threshold"
    
    self.proxy_list.sort(key=lambda Proxy: Proxy.score, reverse=True)
    if len(self.master_proxy_list) < 10:
      for proxy in self.proxy_list:
        if proxy.score < 100:
          self.proxy_list.remove(proxy)
          print("\n Removed Proxys with score <= 100 \n")
        elif proxy.score >= 100 and len(self.master_proxy_list) < 10:
          self.master_proxy_list.append(proxy)
      

    self.master_proxy_list.sort(key=lambda Proxy: Proxy.score, reverse=True)
    self.proxy_list.clear()

  async def refresh_proxy_list(self,counter,input_proxy_number,input_evaluation_rounds,data_size ):
        
        "A method to refill the proxy list with new evaluated Proxys score > 100"

        if self.ready_for_connection == False:
            if len(self.master_proxy_list) < 10: 
                print("Refreshing the Proxy List \n")
                await asyncio.sleep(3)
                print("Refreshing the Proxy List \n")
                
                await asyncio.gather(self.fetch_proxys_write_to_class(input_proxy_number,input_evaluation_rounds,data_size))
                await asyncio.gather(self.evaluate_proxy_list(counter, input_evaluation_rounds,data_size, input_proxy_number))
                

                await self.sort_proxy_lists()

                if len(self.master_proxy_list) < 10:
                    await self.refresh_proxy_list(counter,input_proxy_number,input_evaluation_rounds,data_size )
                else:
                    self.ready_for_connection = True
                    

            else:
                self.ready_for_connection = True
                await self.sort_proxy_lists()
                print(f"{self.protocol}  *** MASTER *** Proxy List is ready for Connection")
                
        else:
          
          print(f"{self.protocol}  *** MASTER *** Proxy List is ready for Connection")
                
      