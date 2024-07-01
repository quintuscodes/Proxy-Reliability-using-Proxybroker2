
from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.inet import TCP
import asyncio
from concurrent.futures import ThreadPoolExecutor

"""
A Class for managing a single proxy fetched from the proxybroker2 python tool.
"""

class Proxy:

  def __init__(self,_proto,_ip,_port,_handshakes):
    self.protocol = _proto
    self.ip = _ip
    self.port =_port
    self.score = 0
    self.handshakes = _handshakes
    self.log_handshake = []
    self.log_syn_ack_time = []
    self.avg_syn_ack_time = 0
    self.log_transmission_time = []
    self.avg_transmission_time = 0
    self.log_throughput = []
    self.avg_throughput = 0
    
    
    
    
    

    """
    A Class for managing a single proxy fetched from the proxybroker2 python tool.
    """

    print(f"Initiated Proxy: \nIP: {self.ip}   , Port:  {self.port},  Protokoll:  {self.protocol}, ")

  #TODO Getter and Setter for Proxy
  def get_object(self):
     
     return self
  
  def get_ip(self):
    return self.ip
  
  def get_port(self):
    return self.port
  
  def get_score(self):
    return self.score

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

  def set_log_handshake(self,n):
    self.log_handshake.append(n)

  def set_log_syn_ack_time(self,syn_ack):
    self.log_syn_ack_time.append(syn_ack)

  def set_log_transmission_time(self,transm_time):
    self.log_transmission_time.append(transm_time)

  def set_log_throughput(self,throughput):
    self.log_throughput.append(throughput)
    

  def add_to_list(self,proxy_list):
    proxy_list.append(self)
    
    attrs = vars(self)
    print(f"\nAdded to List:\n" + ', \n'.join("%s: %s" % item for item in attrs.items()) + "\n")

  async def send_paket(self,packet,timeout=2):
    loop = asyncio.get_running_loop()
    try:
       future =  loop.run_in_executor(None, sr1, packet)
       return await asyncio.wait_for(future,timeout)
    
    except asyncio.TimeoutError:
      print(f"TimeoutError: Keine Antwort vom Proxy {self.ip}:{self.port} erhalten.")
      return None

  
  
  async def master_evaluate(self,index,queue,proxy_list):
    #Worker Function to call async Task Group evaluate functions asynchronously 
    
    while True:
     
      print(f"------------------------------START MASTER EVALUATE fuer {index}. Proxy mit IP: {self.ip} und PORT: {self.port}----------------------------\n")
      print(queue)
      #TODO Schedule Tasks with Asyncio to perform evaluation concurrently
    
      task = await queue.get()

      try:
        await task()

      except Exception as e:
                print(f"Error während der Ausführung des Tasks: {e}")
      
      finally:
         queue.task_done()
    
     

      
      
  async def evaluate(self):
     #Asynchron Wrapping um Thread Pool Executor der synchronen Evaluierungsmethoden
    loop = asyncio._get_running_loop()
    with ThreadPoolExecutor() as pool:
       await loop.run_in_executor(pool, self.evaluate_handshakes)
       await loop.run_in_executor(pool,self.evaluate_throughput)
       await loop.run_in_executor(pool,self.evaluate_transmission_time)
       



  def evaluate_handshakes(self):
      "Evaluate a successful TCP-Handshake Hit Ratio and the Time for establishing the handshake"
      print(f"START HANDSHAKE PROT: {self.protocol} IP:  {self.ip}  PORT:  {self.port}\n")
    
    
     # Create SYN-Paket to Proxy
      syn_packet = IP(dst=self.ip) / TCP(dport=self.port, flags="S")
      print("Erstelle SYN- Paket: \n")

      
      # Transceive SYN-Paket and Receive Answer
      print("Sendet SYN- Paket\n")
      syn_ack_response = sr1(syn_packet,timeout=2,verbose=False)
      #syn_ack_response = sr1(syn_packet, timeout=2, verbose=False)
      
      #TODO dieses if statement erneut anschauen
      if syn_ack_response:
          syn_ack_time = syn_ack_response.time - syn_packet.sent_time
          print(f"Response time for SYN-ACK: {syn_ack_time} seconds")
          

          if syn_ack_response.haslayer(TCP) and syn_ack_response[TCP].flags & 0x12:
              print("SYN-ACK empfangen. Handshake erfolgreich.\n")

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
              self.set_log_syn_ack_time(syn_ack_time)
              print(f"Log SYN_ACK set to \n {self.get_log_syn_ack_time()}\n")
              
              
      else:
          print("Keine Antwort empfangen. Handshake fehlgeschlagen.\n")
          
          self.set_log_handshake(0)
          print(f"Log Handshake set to \n {self.get_log_handshake()}\n")
          self.set_log_syn_ack_time(1)
          print(f"Log SYN_ACK set to \n {self.get_log_syn_ack_time()}\n")
      
      

  def evaluate_transmission_time(self):
    "Evaluate the transmission time for sending (1000Bytes)data size packets and receiving a answer."
    print(f"START TTM PROT: {self.protocol} IP:  {self.ip}  PORT:  {self.port}\n")
    
    #Data Packet for Measuring Transmission Time of 1000 Bytes of data
    data_size = 1000
    data_packet = IP(dst=self.ip)/TCP(dport=self.port)/Raw(RandString(size=data_size))
    start_time = time.time()
    #response = await self.send_paket(data_packet,timeout=2)
    response = sr1(data_packet, timeout=5,verbose=False)
    end_time = time.time()

    if response:
        transmission_time = end_time - start_time
        print(f"Transmission time for {data_size} bytes of data: {transmission_time} seconds")
        self.set_log_transmission_time(transmission_time)
        print(f"Log Transmission TIme set to \n {self.get_log_transmission_time()}\n")
        
    else:
        print("No response received.")
  
        self.set_log_transmission_time(1)
        print(f"Log Transmission TIme set to \n {self.get_log_transmission_time()}\n")

   
      
  
  def evaluate_throughput(self):
    "Evaluate Time for sending 10 Packets a 1kB - TODO is this necessary?, because it actually tests the physical layer not the proxy reliability?"
    print(f"START Throughput PROT: {self.protocol} IP:  {self.ip}  PORT:  {self.port}\n")
    
    # Data Packet for Measuring Throughput
    data_size = 1000
    throughput_packet = IP(dst=self.ip)/TCP(dport=self.port)/Raw(RandString(size=data_size))

    #Send 10 data packets to proxy and measure time for 10 * 1000Bytes
    start_time = time.time()

    
    for packet in range(10):
          send(throughput_packet,verbose=False)
    
      #await asyncio.gather(*[send_paket(throughput_packet) for send in range(10)])

    end_time = time.time()

      # Calculate throughput
    total_data_size = data_size * 10
    throughput = total_data_size / (end_time - start_time)
    print(f"Throughput: {throughput / 1000} KBytes per second")

    throughput = throughput / 1000
    if self.get_last_log_handshake_item() == 0:
       self.set_log_throughput(0)
    else:
       self.set_log_throughput(throughput)

    print(f"Log Throughput set to \n {self.get_log_throughput()} in KB/second \n")
     
    

  def calc_score(self,input_evaluation_rounds):
    """
    A function to calculate the score given the parameters TCP Handshake Hit Ratio, [Syn_ACK] Response Time, Transmission Time, Throughput
    """
    succ_handshakes = self.log_handshake.count(1)
    handshake_rate = succ_handshakes / input_evaluation_rounds
    score = handshake_rate * 100
    self.score = score

    #TODO Calculate SYN-ACK Score Add Bonus of 3 Best Avg_resp_time to score ; 15 , 10 , 5 points
    sum_syn_ack = sum(self.log_syn_ack_time)
    avg_syn_ack_time = sum_syn_ack / input_evaluation_rounds
    self.avg_syn_ack_time = avg_syn_ack_time
    if self.avg_syn_ack_time == 0.0:
        self.avg_syn_ack_time = 99
    #self.log_syn_ack_time.clear()

    #TODO calc AVG transmission time for data size - 1000B default
    sum_transmission_time = sum(self.log_transmission_time)
    avg_transmission_time = sum_transmission_time / input_evaluation_rounds
    self.avg_transmission_time = avg_transmission_time
    if self.avg_transmission_time == 0.0:
      self.avg_transmission_time = 99
    #self.log_transmission_time.clear()

    "calc AVG Throughput score"
    sum_throughput = sum(self.log_throughput)
    avg_throughput = sum_throughput / input_evaluation_rounds
    self.avg_throughput = avg_throughput
    