
from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.inet import TCP
import asyncio
from concurrent.futures import ThreadPoolExecutor
import requests
import time
import os



class Proxy:

  """
  A Class for managing a single proxy fetched from the proxybroker2 python tool.
  """

  def __init__(self,_proto: str,_ip,_port:int,_country:str,_handshakes:int):
    self.protocol = _proto
    self.ip = _ip
    self.port =_port
    self.avg_score = 0
    self.score = 0
    self.log_score = []
    self.country = _country
    self.handshakes = _handshakes
    self.log_handshake = []
    self.log_syn_ack_time = []
    self.avg_syn_ack_time = 0
    self.log_transmission_time = []
    self.avg_transmission_time = 0
    self.log_throughput = []
    self.avg_throughput = 0
    self.log_request = []
    "Rates added for plotting"
    self.request_rate = 0
    self.handshake_rate = 0

    print(f"Initiated Proxy: \nIP: {self.ip}   , Port:  {self.port},  Protokoll:  {self.protocol}, ")

  "Getter and Setter for Proxy"
  def get_avg_transmission_time(self):
     return self.avg_transmission_time
  
  def get_avg_syn_ack_time(self):
     return self.avg_syn_ack_time
  
  def get_avg_throughput(self):
     return self.avg_throughput
  
  def get_request_rate(self):
     return self.request_rate
  
  def get_handshake_rate(self):
     return self.handshake_rate
  
  def get_object(self):
     
     return self
  
  def get_ip(self):
    return self.ip
  
  def get_port(self):
    return self.port
  
  def get_score(self):
    return self.score
  
  def get_avg_score(self):
     return self.avg_score
  
  def get_last_log_handshake_item(self):
     last_elem = self.log_handshake[-1]
     return last_elem
  
  def get_log_handshake(self):
    return self.log_handshake
  
  def get_log_syn_ack_time(self):
    return self.log_syn_ack_time
  
  def get_log_transmission_time(self):
    return self.log_transmission_time
  
  def get_log_throughput(self):
    return self.log_throughput
  
  def set_score(self, _score):
    self.score = _score

  def set_avg_score(self):
    sum_score = sum(self.log_score)
    denom = len(self.log_score)
    if denom == 0:
       self.avg_score = self.score
    else:
      self.avg_score = sum_score / denom
  def set_rates(self):
    self.request_rate = (self.log_request.count(200) / self.handshakes) *100
    self.handshake_rate = (self.log_handshake.count(1) / self.handshakes) * 100
     
  def set_log_score(self):
     self.log_score.append(self.score)

  def set_log_handshake(self,n):
    self.log_handshake.append(n)

  def set_log_syn_ack_time(self,syn_ack):
    self.log_syn_ack_time.append(syn_ack)

  def set_log_transmission_time(self,transm_time):
    self.log_transmission_time.append(transm_time)

  def set_log_throughput(self,throughput):
    self.log_throughput.append(throughput)
     
  def set_log_request(self,res):
     self.log_request.append(res)

  def reset_attributes(self):
    self.score = 0
    self.log_handshake = []
    self.log_syn_ack_time = []
    self.avg_syn_ack_time = 0
    self.log_transmission_time = []
    self.avg_transmission_time = 0
    self.log_throughput = []
    self.avg_throughput = 0
    self.log_request = []
    self.request_rate = 0
    self.handshake_rate = 0
    
 
  async def evaluate(self):
    """
    Method to evaluate proxys of the proxy list concurrently using a ThreadPoolExecutor and asyncio

            - synchronous methods will be wrapped in an asynchronous Executor

    """

    loop = asyncio._get_running_loop()
    with ThreadPoolExecutor() as pool:
       await loop.run_in_executor(pool, self.evaluate_handshakes)
       print(f"Completed Handshake evaluation for {self.ip}")
       await loop.run_in_executor(pool,self.evaluate_throughput)
       print(f"Completed Throughput evaluation for {self.ip}")
       await loop.run_in_executor(pool,self.evaluate_request)
       print(f"Completed Request evaluation for {self.ip}")
       



  def evaluate_handshakes(self):
      
      "Evaluate a (successful) TCP-Handshake Hit Ratio and the Time for establishing the handshake -> syn_ack_time"

      print(f"START HANDSHAKE PROT: {self.protocol} IP:  {self.ip}  PORT:  {self.port}\n")
    
    
      # Create SYN-Paket to Proxy
      syn_packet = IP(dst=self.ip) / TCP(dport=self.port, flags="S")
      print("Erstelle SYN- Paket: \n")

      
      # Transceive SYN-Paket and Receive Answer
      print("Sendet SYN- Paket\n")
      start_time = time.time()
      syn_ack_response = sr1(syn_packet,timeout=2,verbose=False)
      end_time = time.time()
      
      
      if syn_ack_response:
          
          if syn_ack_response.haslayer(TCP) and syn_ack_response[TCP].flags & 0x12:
              print("SYN-ACK empfangen. Handshake erfolgreich.\n")
              syn_ack_time = syn_ack_response.time - syn_packet.sent_time
              print(f"Response time for successful Handshake  SYN-ACK-Time : {syn_ack_time} seconds\n")

          # Create ACK-Paket to Proxy

              ack_packet = IP(dst=self.ip) / TCP(dport=self.port, flags="A",
                                                seq=syn_ack_response[TCP].ack,
                                                ack=syn_ack_response[TCP].seq + 1)
              
          #Display Paket Answer to console

              #print("Die Antwort:\n")
              #syn_ack_response.show() 

          # Send ACK-Paket to Proxy
              send(ack_packet)
              print("ACK gesendet. Handshake abgeschlossen.\n")
              
              self.set_log_handshake(1)
              print(f"Log Handshake set to \n {self.get_log_handshake()}\n")
              self.set_log_syn_ack_time(syn_ack_time)
              print(f"Log SYN_ACK set to \n {self.get_log_syn_ack_time()}\n")
              
          else:
              print("SYN-ACK nicht empfangen. Handshake fehlgeschlagen.\n")
              self.set_log_handshake(0)
              print(f"Log Handshake set to \n {self.get_log_handshake()}\n")
              self.set_log_syn_ack_time(1) #float('inf') otherwise
              print(f"Log SYN_ACK set to \n {self.get_log_syn_ack_time()}\n")
              
              
      else:
          print("Keine Antwort empfangen. Handshake fehlgeschlagen.\n")
          
          self.set_log_handshake(0)
          print(f"Log Handshake set to \n {self.get_log_handshake()}\n")
          self.set_log_syn_ack_time(1) # float('inf') otherwise
          print(f"Log SYN_ACK set to \n {self.get_log_syn_ack_time()}\n")
      
    


  def evaluate_throughput(self):

    "Evaluate Throughput using the Proxy performing a http-Request and sending 1MB of random Data through the Proxy. "

    print(f"START Throughput PROT: {self.protocol} IP:  {self.ip}  PORT:  {self.port}\n")
    
    
    url = "https://httpbin.org/post"

    proxy_requ = {
                "http": f"http://{self.ip}:{self.port}"
    }
    data_block = os.urandom(1024 * 1024) # 1 MB of random data
    

    "Sending the Data Block through the proxy using the http post method"
    try:
       
      start_time = time.time()
      response = requests.post(url, data=data_block, proxies=proxy_requ, timeout=30)
      end_time = time.time()

      if response.status_code == 200:
         data_sent = len(data_block)
         data_received = len(response.content)
         total_data_size = data_sent + data_received

         throughput = total_data_size / (end_time - start_time)
         self.set_log_throughput(throughput / 1024) #KB/s
         print(f"Throughput: {throughput / 1024} KB/s")
      else:
         print(f"Throughput HTTP request failed with status code: {response.status_code}")
         self.set_log_throughput(0) # Low Value for Fail Indication in Scoring

    except requests.ReadTimeout:
        print("HTTP request timed out.")
        self.set_log_throughput(0)  # high value to indicate fail
        

    except requests.RequestException as e:
      print(f"HTTP request through proxy failed: {e}")
      self.set_log_throughput(0) # Low Value for Fail Indication in Scoring

    
    print(f"Log Throughput set to \n {self.get_log_throughput()} in KB/s \n")

  def evaluate_request(self):
    
    "Method to perform an HTTP request and evaluate the proxy based on response time and status code."

    proxy_requirements_urls = {
            "http" : f"http://{self.ip}:{self.port}"
     }
    
    
    
    data_block = os.urandom(1024 * 1024) # 1 MB of random data
    
    try:

      start_time = time.perf_counter()
      response = requests.get("https://httpbin.org/get",data=data_block,proxies=proxy_requirements_urls,timeout=30)
      end_time = time.perf_counter()
      transmission_time = end_time - start_time

      if response.status_code == 200:
         print(f"HTTP request successful. Response time: {transmission_time} seconds")
         self.set_log_transmission_time(transmission_time) 
         self.set_log_request(200) # log success
      else:
         print(f"HTTP request failed with status code : {response.status_code}")
         self.set_log_transmission_time(1) #float('inf')
         self.set_log_request(response.status_code) # fail 

    except requests.ReadTimeout:
        print("HTTP request timed out.")
        self.set_log_transmission_time(1)  # high value to indicate fail float('inf')
        self.set_log_request(408)  # HTTP 408 Request Timeout

    except requests.RequestException as fail:
       print(f"HTTP request failed: {fail} ")
       self.set_log_transmission_time(1) #high value to indicate fail float('inf')
       self.set_log_request(500) #fail
    

  def calc_score(self,evaluation_rounds):
    """
    Method to calculate the score given the parameters TCP Handshake Hit Ratio, [Syn_ACK] Response Time, Transmission Time, Throughput and Requests Ratio
    """
    succ_handshakes = self.log_handshake.count(1)
    handshake_rate = succ_handshakes / evaluation_rounds
    handshake_score = (handshake_rate * 100) / 2
    self.score += handshake_score
    self.handshake_rate = handshake_rate * 100
    self.log_handshake.clear()

    "Calculate avg_syn_ack"
    sum_syn_ack = sum(self.log_syn_ack_time)
    avg_syn_ack_time = sum_syn_ack / evaluation_rounds
    self.avg_syn_ack_time = avg_syn_ack_time
    if self.avg_syn_ack_time == 0.0:
        self.avg_syn_ack_time = float('inf')
    self.log_syn_ack_time.clear() # Comment out/in if you want to print log to console

    "Calc avg_TransmissionTime"
    sum_transmission_time = sum(self.log_transmission_time)
    avg_transmission_time = sum_transmission_time / evaluation_rounds
    self.avg_transmission_time = avg_transmission_time
    if self.avg_transmission_time == 0.0:
      self.avg_transmission_time = 1 #float('inf')
    self.log_transmission_time.clear() # Comment out/in if you want to print log to console

    "calc AVG Throughput"
    sum_throughput = sum(self.log_throughput)
    avg_throughput = sum_throughput / evaluation_rounds
    self.avg_throughput = avg_throughput
    self.log_throughput.clear() # Comment out/in if you want to print log to console
    
    "Request Score"
    succ_requests = self.log_request.count(200)
    requests_rate = succ_requests / evaluation_rounds
    requ_score = (requests_rate * 100) / 2
    self.score += requ_score
    self.request_rate = requests_rate *100
    self.log_request.clear()

    "Failed Requests - Punish failed requests "

    failed_requ = evaluation_rounds - succ_requests
    penalty = failed_requ * 5
    self.score -= penalty
    #print(f"Penalty of {penalty} Points to {self.ip} deducted. ")

    
    