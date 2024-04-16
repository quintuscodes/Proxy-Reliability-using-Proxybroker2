
"""
This is the class for managing a single proxy 
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
    
    print(f"Initiated Proxy: \nIP: {self.ip}   , Port:  {self.port},  Protokoll:  {self.protocol}, ")


  def add_to_list(self,proxy_list):
    proxy_list.append(self)
    
    attrs = vars(self)
    print(f"\nAdded to List:\n" + ', \n'.join("%s: %s" % item for item in attrs.items()) + "\n")
       
