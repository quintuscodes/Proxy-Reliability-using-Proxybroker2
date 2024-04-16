"This is the python class for Proxy Manager"


class Proxy:

  def __init__(self,_ip,_port,_score,_avg_syn_ack_time,_avg_transmission_time,_avg_throughput,_handshakes,_log_handshakes,_log_syn_ack_time,_log_transmission_time,_log_throughput):
    self.ip = _ip
    self.port =_port
    self.score = _score
    self.avg_syn_ack_time = _avg_syn_ack_time
    self.avg_transmission_time = _avg_transmission_time
    self.avg_throughput = _avg_throughput
    self.handshakes = _handshakes
    self.log_handshake = []
    self.log_syn_ack_time = []
    self.log_transmission_time = []
    self.log_throughput = []
    self.proxy_list = []
          
