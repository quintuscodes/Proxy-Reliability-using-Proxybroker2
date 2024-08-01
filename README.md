# Proxy Validation
<br>
Python Scripts are developed to create a dynamic data structure for managing open-source proxy servers using the Python module proxybroker2.
These scripts evaluate the proxy servers concurrently using asyncio, collecting data such as successful TCP-Handshake rate, average response time, average transmission time,  average throughput and perform a request. 
The goal is to evaluate a dynamic proxy list for reliable proxy connections.  <br>
<br>
<br>

# Class Diagram
The portrayed Class Diagram for the Proxy Manager. <br>
<br>
<br>

'''mermaid 
classDiagram
  direction LR
  class Proxy_Manager {
    - ready_for_connection: bool
    - protocol: str
    - master_proxy_list: list
    - proxy_list: list
    - log_evaluation_time: list
    + __init__(_protocol)
    + fetch_proxys_write_to_class(proxy_number, evaluation_rounds)
    + write_proxy_to_class(_type, proxies, evaluation_rounds)
    + add_to_list(Proxy)
    + print_proxy_list(arg)
    + evaluate_proxy_list(counter, evaluation_rounds)
    + sort_proxy_lists(proxy_number)
    + refresh_proxy_list(counter, proxy_number, evaluation_rounds)
    + reset_proxys()
    + log_scores()
  }

  class Proxy {
    - protocol: str
    - country: str
    - ip: str
    - port: int
    - avg_score: int
    - avg_syn_ack_time: float
    - avg_throughput: float
    - avg_transmission_time: float
    - score: int
    - handshakes: int
    - log_handshake: list
    - log_request: list
    - log_score: list
    - log_syn_ack_time: list
    - log_throughput: list
    - log_transmission_time: list
    + __init__(_proto, _ip, _port, _country, _handshakes)
    + evaluate()
    + evaluate_handshakes()
    + evaluate_throughput()
    + evaluate_request()
    + calc_score(evaluation_rounds)
    + get_ip()
    + get_last_log_handshake_item()
    + get_log_handshake()
    + get_log_syn_ack_time()
    + get_log_throughput()
    + get_log_transmission_time()
    + get_object()
    + get_port()
    + get_score()
    + reset_attributes()
    + set_avg_score()
    + set_log_handshake(n)
    + set_log_request(res)
    + set_log_score()
    + set_log_syn_ack_time(syn_ack)
    + set_log_throughput(throughput)
    + set_log_transmission_time(transm_time)
    + set_score(_score)
  }

  Proxy_Manager --> Proxy : manages
'''

# Sequence Diagram
