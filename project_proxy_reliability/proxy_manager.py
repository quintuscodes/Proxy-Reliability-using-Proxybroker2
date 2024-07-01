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
  A Class for Managing Proxy List and Evaluation
  """
  def __init__(self,_protocol):
    self.ready_for_connection = False
    self.protocol = _protocol
    self.master_proxy_list = []
    self.proxy_list = []
    self.proxy_list_slave = []
  

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
      
    await self.print_proxy_list(0)
    





  async def print_proxy_list(self,arg):
    """
    A function to print the actual proxy_list
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
          #print(f', \n'.join("%s: %s" % item for item in attrs.items()) + "\n")
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
      
    
      tasks = []
      print(f"Test Queue Evaluation Round Nr. {counter}")
      

      for i in range(len(self.proxy_list)):
        proxy = self.get_proxy(i)
        task = proxy.evaluate()
        tasks.append(task)
        #task calculate score per proxy
        

      await asyncio.gather(*tasks)
    
    for i in range(len(self.proxy_list)):
        proxy = self.get_proxy(i)
        proxy.calc_score(input_evaluation_rounds)

    "Reward the Best Proxys in evaltuation parameters - sort then give 15,10,5 Points credit score"
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
    

    
    """
        queue.put_nowait(proxy.evaluate_handshakes)

        print("Queue Evaluate Handshake added")

        queue.put_nowait(proxy.evaluate_throughput)

        print("Queue Evaluate Throughput added")

        queue.put_nowait(proxy.evaluate_transmission_time)

        print("Queue Evaluate TTM added\n")
  
      for i in range(len(self.proxy_list)):
          index = i + 1

          proxy = self.get_proxy(i)
          
          
          
          
          print(queue.qsize())
          await proxy.master_evaluate(index,queue,self.proxy_list)
          #task = asyncio.create_task()
          print(f"Master Evaluate Proxy Task created - evaluate async Proxy IP: {proxy.ip} ")
          #tasks.append(task)
          
        
      await queue.join() 

      for task in tasks:
        task.cancel()
        # Wait until all worker tasks are cancelled.
      
      await asyncio.gather(*tasks, return_exceptions=True)
      
      """



    #calc_score(proxy_list,input_evaluation_rounds)  
    #print_proxy_list_dict(proxy_list) 

    """
    for proxy in proxy_list:
      async create task(proxy.master_evaluate)
    """
  async def sort_proxy_lists(self):
    """A Function for sorting the List and remove proxys with a 70 score threshold
    """
    #TODO SORT first, so that proxy with score 100 is on top
    
    self.proxy_list.sort(key=lambda Proxy: Proxy.score, reverse=True)

    
    unbalanced = True
    
        
    #DELETE Proxys with score < 60
    while unbalanced and len(self.proxy_list) > 0:
        for proxy in self.proxy_list:
            if proxy.score <= 100:
                self.proxy_list.remove(proxy)
                print("\n Removed Proxys with score <= 100 \n")
                
                await self.sort_proxy_lists()
            
            else: unbalanced = False
    "Looping the Proxy List and Copy proxys with score > 100 of proxy_list -> Master proxy_list"
    
    for proxy in self.proxy_list:
           
      if proxy.score >= 100:
              self.master_proxy_list.append(proxy)
    self.master_proxy_list.sort(key=lambda Proxy: Proxy.score, reverse=True)
    self.proxy_list.clear()

  async def refresh_proxy_list(self,counter,input_proxy_number,input_evaluation_rounds,data_size ):
        master = "master"
        "A function to refill the proxy list with new evaluated Proxys"
        """
                TODO: 
                
                - gather 5 new!!!(check if IPs are not doubled) proxys to empty self.proxy_list
                - evaluate them and push with score > 120 in the self.master_list

                - checker method every asyncio.sleep(5) seconds to listen if 10 reliable proxys are in the list, if not -> refresh list 
                
        """

        if self.ready_for_connection == False:
            if  len(self.master_proxy_list) <= 10: 
                print("Refreshing the Proxy List \n")
                #asyncio.sleep(5)
                print("Refreshing the Proxy List \n")
                
                await asyncio.gather(self.fetch_proxys_write_to_class(input_proxy_number,input_evaluation_rounds,data_size))
                await asyncio.gather(self.evaluate_proxy_list(counter, input_evaluation_rounds,data_size, input_proxy_number))
                

                self.sort_proxy_lists()

                if len(self.master_proxy_list) <= 7:
                    self.refresh_proxy_list(counter,input_proxy_number,input_evaluation_rounds,data_size )
                else:
                    self.ready_for_connection = True
                    self.refresh_proxy_list(counter,input_proxy_number,input_evaluation_rounds,data_size )

            else:
                self.ready_for_connection = True
                self.sort_proxy_list()
                print("*** MASTER *** Proxy List is ready for Connection")
        else:
          
          print("*** MASTER *** Proxy List is ready for Connection")
                
      