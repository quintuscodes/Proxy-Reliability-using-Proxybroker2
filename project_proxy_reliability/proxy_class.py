"This is the python class for Proxy Manager"


class Proxy:

  def __init__(self,ip,port,score,avg_syn_ack_time,avg_transmission_time,avg_throughput,handshakes,log_handshakes,log_syn_ack_time,log_transmission_timelog_throughput):
    self.ip = 0
    self.port = 0
    self.score = 0
    self.avg_syn_ack_time = 0
    self.avg_transmission_time = 0
    self.avg_throughput = 0
    self.handshakes = 0
    self.log_handshake = []
    self.log_syn_ack_time = []
    self.log_transmission_time = []
    self.log_throughput = []
          
