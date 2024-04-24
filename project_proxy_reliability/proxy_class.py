
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

    #Params for request eval

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

  """
  async def master_evaluate(self):
    #Function to call async Task Group evaluate functions  - not sure to declare here or in proxy_Manager

  
  async def evaluate_handshakes(self):
     #Function to evaluate the handshake

  async def evaluate_transmission_time(self)
    #Function to evaluate the transmission time
  
  async def evaluate_throughput(self)
    #Function to evaluate the througput
  """
  