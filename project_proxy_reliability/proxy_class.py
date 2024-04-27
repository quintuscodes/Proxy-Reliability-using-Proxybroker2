
from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.inet import TCP
import asyncio

"""
A Class for managing a single proxy fetched from the proxybroker2 python tool.
"""

class Proxy:

  def __init__(self,_proto,_ip,_port,_handshakes):
    self.protocol = _proto
    self.ip = _ip
    self.port =_port
    self.score = 0
    self.avg_syn_ack_time = 0
    self.avg_transmission_time = 0
    self.avg_throughput = 0
    self.handshakes = _handshakes
    self.log_handshake = []
    self.log_syn_ack_time = []
    self.log_transmission_time = []
    self.log_throughput = []

    """
    A Class for managing a single proxy fetched from the proxybroker2 python tool.
    """

    print(f"Initiated Proxy: \nIP: {self.ip}   , Port:  {self.port},  Protokoll:  {self.protocol}, ")

  #TODO Getter and Setter for Proxy

  def get_ip(self):
    return self.ip
  
  def get_port(self):
    return self.port
  
  def get_score(self):
    return self.score

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


  
  async def master_evaluate(self,index):
    #Function to call async Task Group evaluate functions asynchronously  - not sure to declare here or in proxy_Manager
    task = asyncio.create_task(print(f"------------------------------START MASTER EVALUATE fuer {index}. Proxy mit IP: {self.ip} und PORT: {self.port}----------------------------\n"))
 
    #TODO Schedule Tasks with Asyncio to perform evaluation concurrently
    
    tasks = [task, self.evaluate_handshakes(),self.evaluate_transmission_time(),self.evaluate_throughput()]

    await asyncio.gather(*tasks)
  
    #asyncio.gather()
    #asyncio Taskgroup 






  async def evaluate_handshakes(self):
     #Coroutine Function to evaluate the handshake

     # Create SYN-Paket to Proxy
      syn_packet = IP(dst=self.ip) / TCP(dport=self.port, flags="S")
      print("Erstelle SYN- Paket: \n")

      
      # Transceive SYN-Paket and Receive Answer
      print("Sendet SYN- Paket\n")
      syn_ack_response = await send_paket(syn_packet)
      #syn_ack_response = sr1(syn_packet, timeout=2, verbose=False)
      
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
          self.set_log_syn_ack_time(0)
          print(f"Log SYN_ACK set to \n {self.get_log_syn_ack_time()}\n")
      
      return self

  async def evaluate_transmission_time(self):
    #Coroutine Function to evaluate the transmission time

    #Data Packet for Measuring Transmission Time of 1000 Bytes of data
    data_size = 1000
    data_packet = IP(dst=self.ip)/TCP(dport=self.port)/Raw(RandString(size=data_size))
    start_time = time.time()
    response = await send_paket(data_packet)
    #response = sr1(data_packet, verbose=False, timeout=5)
    end_time = time.time()

    if response:
        transmission_time = end_time - start_time
        print(f"Transmission time for {data_size} bytes of data: {transmission_time} seconds")
        self.set_log_transmission_time(transmission_time)
        print(f"Log Transmission TIme set to \n {self.get_log_transmission_time()}\n")
        
    else:
        print("No response received.")
        print(f"Transmission time for {data_size} bytes of data: {transmission_time} seconds")
        self.set_log_transmission_time(0)
        print(f"Log Transmission TIme set to \n {self.get_log_transmission_time()}\n")

    return self 
  
  async def evaluate_throughput(self):
    #Coroutine Function to evaluate the througput
    # Data Packet for Measuring Throughput
    data_size = 1000
    throughput_packet = IP(dst=self.ip)/TCP(dport=self.port)/Raw(RandString(size=data_size))

    #Send 10 data packets through proxy and measure time for 10 * 1000Bytes
    start_time = time.time()

    for packet in range(10):
        send(throughput_packet, verbose=False)
    
    #await asyncio.gather(*[send_paket(throughput_packet) for send in range(10)])

    end_time = time.time()

    # Calculate throughput
    total_data_size = data_size * 10
    throughput = total_data_size / (end_time - start_time)
    print(f"Throughput: {throughput / 1000} KBytes per second")

    throughput = throughput / 1000
    self.set_log_throughput(throughput)
    print(f"Log Throughput set to \n {self.get_log_throughput()} in KB/second \n")

    return self
  
async def send_paket(packet):
   return await asyncio.get_event_loop().run_in_executor(None,sr1,packet,verbose=False,timeout=5)
