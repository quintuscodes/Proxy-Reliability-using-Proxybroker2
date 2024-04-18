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
#from requests import *

class Proxy_Manager:

  """
  #proxy_list :: dict/ list
  
  
  """
  def __init__(self,_protocol):
    self.protocol = _protocol
    self.master_proxy_list = []
    self.proxy_list = []




  def perform_request():
    "Perform the Request with [1] in master list"
  
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
            