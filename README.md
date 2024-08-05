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

```mermaid 
%%{init: {'theme':'neutral'}}%%
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
```

# Sequence Diagram

```mermaid 
sequenceDiagram
    participant User
    participant Main
    participant Proxy_Manager
    participant Proxy
    participant Functions

    User->>Main: run(proxy_number, evaluation_rounds, protocols)
    activate Main
    Main->>Main: main(proxy_number, evaluation_rounds, protocols)
    
    Main->>Proxy_Manager: __init__("HTTP")
    Main->>Proxy_Manager: __init__("SOCKS4")
    Main->>Proxy_Manager: __init__("SOCKS5")
    Main->>Proxy_Manager: __init__("CONNECT:25")
    Main->>Proxy_Manager: fetch_proxys_write_to_class(proxy_number, evaluation_rounds)
    activate Proxy_Manager
    Proxy_Manager->>Proxy: __init__(_proto, _ip, _port, _country, _handshakes)
    Proxy_Manager->>Proxy_Manager: add_to_list(Proxy)
    Proxy_Manager-->>Main: return
    deactivate Proxy_Manager

    Main->>Proxy_Manager: evaluate_proxy_list(counter, evaluation_rounds)
    activate Proxy_Manager
    Proxy_Manager->>Proxy: evaluate()
    activate Proxy
    Proxy->>Proxy: evaluate_handshakes()
    Proxy->>Proxy: evaluate_throughput()
    Proxy->>Proxy: evaluate_request()
    deactivate Proxy
    Proxy_Manager->>Proxy: calc_score(evaluation_rounds)
    Proxy_Manager-->>Main: return
    deactivate Proxy_Manager

    Main->>Functions: sort_proxy_managers(proxy_managers_list, proxy_number)
    activate Functions
    Functions->>Proxy_Manager: sort_proxy_lists(proxy_number)
    deactivate Functions

    Main->>Functions: Checker(proxy_managers_list, refresh_tasks, proxy_number, num_proto)
    activate Functions
    Functions->>Proxy_Manager: refresh_proxy_list(counter, proxy_number, evaluation_rounds)
    deactivate Functions

    Main->>Functions: rec_wait_and_evaluate_again(proxy_managers_list, counter, evaluation_rounds, proxy_number)
    activate Functions
    Functions->>Functions: log_scores(proxy_managers_list)
    Functions->>Proxy_Manager: reset_proxys()
    Functions->>Functions: generate_evaluate_tasks(proxy_managers_list, counter, evaluation_rounds, proxy_number)
    deactivate Functions
    Main->>Functions: print_proxy_managers(proxy_managers_list, "master")
    Main->>Functions: print_proxy_managers(proxy_managers_list, "slave")
    deactivate Main
```
