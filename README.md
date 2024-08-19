# Proxy Validation
<br>
Python Scripts are developed to create a dynamic data structure for managing open-source proxy servers using the Python module proxybroker2.
These scripts evaluate the proxy servers concurrently using asyncio, collecting data such as successful TCP-Handshake rate, average response time, average transmission time,  average throughput and perform a request. 
The goal is to evaluate a dynamic proxy list for reliable proxy connections.  <br>
<br>
<br>

# Class Diagram
The portrayed Class Diagram for the proxy Manager. <br>
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
    + add_to_list(proxy)
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
    autonumber
    actor main as "CLI - main"
    
    participant socks5 as "SOCKS5   :Proxy_Manager"
    participant http as "HTTP   :Proxy_Manager"
    participant broker as "Broker   :proxybroker"
    participant proxy as Proxy
    participant functions as Functions

    
    main->>main: run(proxy_number: int, evaluation_rounds: int, protocols: set)
    main->>main: asyncio.get_event_loop()
    loop
      activate main
      main->>main: loop.run_until_complete(main(proxy_number, evaluation_rounds, protocols))
      
      
      main->>+http: new   Proxy_Manager("HTTP")
      http-->> main: http
      main->>main: fetch_tasks.append(http.fetch_proxy_write_to_class())
      main->>main: evaluate_tasks.append(http.evaluate_proxy_list())
      main->>main: refresh_tasks.append(http.refresh_proxy_list())

      main->>+socks5: new   Proxy_Manager("SOCKS5")
      socks5-->>main: socks5

      main->>main: fetch_tasks.append(socks5.fetch_proxy_write_to_class())
      main->>main: evaluate_tasks.append(socks5.evaluate_proxy_list())
      main->>main: refresh_tasks.append(socks5.refresh_proxy_list())
      
      main->>main: await asyncio.gather(*fetch_tasks)
      par fetch http
          
        main-)http: fetch_proxys_write_to_class()
        http-)+broker: new   Broker()
        broker-)broker: find(protocol,lvl = 'HIGH',limit=proxy_num)
        http-)http: write_proxy_to_class()
        http-)+proxy: new   proxy(type,ip,port,country,evaluation_rounds)
        proxy->>http: add_to_list(<proxy>)
        deactivate broker
      and fetch socks5
        main-)socks5: fetch_proxys_write_to_class()
        socks5-)+broker: new   Broker()
        broker-)broker: find(protocol,lvl = 'HIGH',limit=proxy_num)
        socks5-)socks5: write_proxy_to_class()
        socks5-)proxy: new   proxy(type,ip,port,country,evaluation_rounds)
        proxy->>socks5: add_to_list(<proxy>)
        deactivate broker
      end

      main->>main: await asyncio.gather(*evaluate_tasks)
      par evaluate http
          
        main-)http: http.evaluate_proxy_list()
        loop evaluation_rounds
          par evaluate proxys concurrently with asyncio
            http-)proxy: proxy.evaluate()
            par
              proxy-)proxy: evaluate_handshakes()
              proxy-)proxy: evaluate_throughput()
              proxy-)proxy: evaluate_request()
            end
            proxy->>proxy: proxy.calc_score()
            proxy-->>http: return
            http->>http: reward_best_proxys()
          end
        end
        
      and evaluate socks5
        main-)socks5: socks5.evaluate_proxy_list()
        loop evaluation_rounds
          par evaluate proxys concurrently with asyncio
            socks5-)proxy: proxy.evaluate()
            par
              proxy-)proxy: evaluate_handshakes()
              proxy-)proxy: evaluate_throughput()
              proxy-)proxy: evaluate_request()
            end
            proxy->>proxy: proxy.calc_score()
            proxy-->>http: return
            socks5->>socks5: reward_best_proxys()
          end
        end
      end
      

      main->>main: await sort_proxy_managers()
      loop
        
        Note right of main: Remove Proxys with score <100
        main->>http:sort_proxy_lists()
        main->>socks5: sort_proxy_lists()
      end 
      
      main->>functions:await rec_wait_and_evaluate_again()
      functions->>http: log_scores()
      functions->>socks5: log_scores()
      functions->>main: await print_proxy_managers()
      loop
        Note over functions: Wait 20s
      end
      functions->>functions: await Checker()
      loop
        alt CHECK APPROVED
          
        else CHECK Reject - Refill
          functions-)functions: await asyncio.gather(*refresh_tasks)
          functions-)http: http.refresh_proxy_list()
          functions-)socks5: socks5.refresh_proxy_list()
          end
      end
      functions->>functions: reset_proxy_objects()
      par Refresh HTTP Proxy List
        functions->>http: reset_proxys()
        
      and Refresh SOCKS5 Proxy List
        functions->>socks5: reset_proxys()
      end

      functions-)functions: await asyncio.gather(*re_evaluate_tasks)
      
      

      deactivate proxy
      deactivate http
      deactivate socks5
      deactivate main
    end
    
```

