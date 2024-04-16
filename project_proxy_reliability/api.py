"""Find and show 10 working SOCKS5 proxies and evaluate them individually via successful TCP-Handshake rate(Availability), average response time, transmission time(1000Bytes), and throughput(10 Packets á 1000 Bytes).
    Goal is to evaluate a dynamic Proxy List for reliable Proxy-Connections."""

from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.inet import TCP
import asyncio
from proxybroker import Broker, Proxy

#from requests import *

def evaluate(ip, port, proxy_list,counter,data_size):
    print(f"#################################################### {counter} . RUNDE ###########################################################")
# Target IP and Port Adress from gathered Proxy List
    target_ip = ip
    target_port = port



    #Data Packet for Measuring Transmission Time of 1000 Bytes of data
    data_size = 1000
    data_packet = IP(dst=target_ip)/TCP(dport=target_port)/Raw(RandString(size=data_size))
    start_time = time.time()
    response = sr1(data_packet, verbose=False, timeout=5)
    end_time = time.time()

    if response:
        transmission_time = end_time - start_time
        print(f"Transmission time for {data_size} bytes of data: {transmission_time} seconds")
        
        for elements in proxy_list:
            if elements.get("ip") == target_ip and elements.get("port") == target_port:
                    
                    elements["log_transmission_time"].append(transmission_time)
                    
                    x = elements.get("log_transmission_time")
                    print(f"Log Transmission TIme set to \n {x}\n")
    else:
        print("No response received.")
        
        for elements in proxy_list:
            if elements.get("ip") == target_ip and elements.get("port") == target_port:
                    
                    elements["log_transmission_time"].append(0)
                    
                    x = elements.get("log_transmision_time")
                    print(f"Log Transmission TIme set to \n {x}\n")

    # Data Packet for Measuring Throughput
    throughput_packet = IP(dst=target_ip)/TCP(dport=target_port)/Raw(RandString(size=data_size))

    #Send 10 data packets through proxy and measure time for 10 * 1000Bytes
    start_time = time.time()
    for packet in range(10):
        send(throughput_packet, verbose=False)
    end_time = time.time()

    # Calculate throughput
    total_data_size = data_size * 10
    throughput = total_data_size / (end_time - start_time)
    print(f"Throughput: {throughput / 1000} KBytes per second")

    for elements in proxy_list:
            if elements.get("ip") == target_ip and elements.get("port") == target_port:
                    throughput = throughput / 1000
                    elements["log_throughput"].append(throughput)
                    
                    x = elements.get("log_throughput")
                    print(f"Log Throughput set to \n {x} in KB/second \n")


# Create SYN-Paket to Proxy
    syn_packet = IP(dst=target_ip) / TCP(dport=target_port, flags="S")
    print("Erstelle SYN- Paket: \n")
    #syn_packet.show()

# Transceive SYN-Paket and Receive Answer
    print("Sendet SYN- Paket\n")
    syn_ack_response = sr1(syn_packet, timeout=2, verbose=False)
    


    if syn_ack_response:
        syn_ack_time = syn_ack_response.time - syn_packet.sent_time
        print(f"Response time for SYN-ACK: {syn_ack_time} seconds")
        

        if syn_ack_response.haslayer(TCP) and syn_ack_response[TCP].flags & 0x12:
            print("SYN-ACK empfangen. Handshake erfolgreich.\n")

        # Create ACK-Paket to Proxy

            ack_packet = IP(dst=target_ip) / TCP(dport=target_port, flags="A",
                                              seq=syn_ack_response[TCP].ack,
                                              ack=syn_ack_response[TCP].seq + 1)
            
        #Display Paket Answer to console

            #print("Die Antwort:\n")
            #syn_ack_response.show() 

        # Send ACK-Paket to Proxy
            send(ack_packet)
            print("ACK gesendet. Handshake abgeschlossen.\n")
            
            for elements in proxy_list:
                if elements.get("ip") == target_ip and elements.get("port") == target_port:
                    
                    elements["log_handshake"].append(1)#log successful handshake
                    elements["log_syn_ack_time"].append(syn_ack_time)
                    x = elements.get("log_handshake")
                    print(f"Log Handshake set to \n {x}\n")
        else:
            print("SYN-ACK nicht empfangen. Handshake fehlgeschlagen.\n")
            
            for elements in proxy_list:
                if elements.get("ip") == target_ip and elements.get("port") == target_port:
                    elements["log_syn_ack_time"].append(syn_ack_time)
                    elements["log_handshake"].append(0)#log unsuccessful handshake
                    x = elements.get("log_handshake")
                    print(f"Log Handshake set to \n {x}\n")
            
    else:
        print("Keine Antwort empfangen. Handshake fehlgeschlagen.\n")
        
        for elements in proxy_list:
            if elements.get("ip") == target_ip and elements.get("port") == target_port:
                    
                    elements["log_handshake"].append(0)#log unsuccessful handshake
                    elements["log_syn_ack_time"].append(0)
                    x = elements.get("log_handshake")
                    print(f"Log Handshake set to \n {x}\n")

def calc_score(proxy_list,input_handshake_tries):
    """
    A function to calculate the score given the parameters TCP Handshake Hit Ratio, [Syn_ACK] Response Time, Transmission Time, Throughput
    """

    
    for elements in proxy_list:
    #Calculate TCP-Handshake-Rate Score
        succ_handshakes = elements["log_handshake"].count(1)
        handshake_rate = succ_handshakes / input_handshake_tries
        score = handshake_rate * 100
        elements["score"]= score
    #TODO Calculate SYN-ACK Score Add Bonus of 3 Best Avg_resp_time to score ; 15 , 10 , 5 points
        sum_syn_ack = sum(elements["log_syn_ack_time"])
        avg_syn_ack_time = sum_syn_ack / input_handshake_tries
        elements["avg_syn_ack_time"] = avg_syn_ack_time
        if elements["avg_syn_ack_time"] == 0.0:
            elements["avg_syn_ack_time"] = 999
        elements["log_syn_ack_time"].clear()
        #if elements["avg_syn_ack_time"] == 0.0:
           # proxy_list.remove(elements)
    #TODO calc AVG transmission time
        sum_transmission_time = sum(elements["log_transmission_time"])
        avg_transmission_time = sum_transmission_time / input_handshake_tries
        elements["avg_transmission_time"] = avg_transmission_time
        if elements["avg_transmission_time"] == 0.0:
            elements["avg_transmission_time"] = 999
        elements["log_transmission_time"].clear()

    #TODO calc AVG Throughput score
        sum_throughput = sum(elements["log_throughput"])
        avg_throughput = sum_throughput / input_handshake_tries
        elements["avg_throughput"] = avg_throughput
        #if elements["avg_transmission_time"] == 0.0:
        #   elements["avg_transmission_time"] = 999
        #elements["log_transmission_time"].clear()

    
    print("Vor SYN ACK Sortierung \n")
    print_proxy_list_dict(proxy_list)
    

    proxy_list.sort(key=lambda e: e["avg_syn_ack_time"], reverse=False) 
    print("Nach AVG SYN-ACK Sortierung\n")
    print_proxy_list_dict(proxy_list)
    try:
        proxy_list[0]["score"] += 15
        proxy_list[1]["score"] += 10
        proxy_list[2]["score"] += 5
        print("Nach SYN ACK Score Anpassung\n")

    except IndexError:
        print("IndexError Occured!")
    
    finally:
        proxy_list.sort(key=lambda e: e["score"], reverse=True)
        print_proxy_list_dict(proxy_list)
        
    #TODO Transmission Time Score calculation
    proxy_list.sort(key=lambda e: e["avg_transmission_time"], reverse=False)
    print("Nach AVG Transmission Time Sortierung\n")
    print_proxy_list_dict(proxy_list)
    
    try:
        proxy_list[0]["score"] += 15
        proxy_list[1]["score"] += 10
        proxy_list[2]["score"] += 5
        print("Nach AVG Transmission Time Score Anpassung\n")
        print_proxy_list_dict(proxy_list)
        print("Nach Score Sortierung\n")
    
    except IndexError:
        print("Index Error Occurred!")

    finally:
        proxy_list.sort(key=lambda e: e["score"], reverse=True)
        print_proxy_list_dict(proxy_list)

    #TODO AVG Throughput Score calculation
    proxy_list.sort(key=lambda e: e["avg_throughput"], reverse=True)
    print("Nach AVG Throughput Sortierung\n")
    print_proxy_list_dict(proxy_list)
    
    try:
        proxy_list[0]["score"] += 15
        proxy_list[1]["score"] += 10
        proxy_list[2]["score"] += 5
        print("Nach AVG Throughput Score Anpassung\n")
        print_proxy_list_dict(proxy_list)
        print("Nach Score Sortierung\n")
    
    except IndexError:
        print("Index Error Occurred!")

    finally:
        proxy_list.sort(key=lambda e: e["score"], reverse=True)
        print_proxy_list_dict(proxy_list)

def evaluate_call(proxy_list,counter, input_handshake_tries,data_size):
  """
  A function to initialize the evaluation of the Proxy 
  """
  while counter < input_handshake_tries: 
    counter += 1 
    for elements in proxy_list:
        index = proxy_list.index(elements)
        index += 1
        targetip =  elements["ip"]
        targetport = elements["port"]
        
        print(f"------------------------------Handshake fuer {index}. Proxy mit IP: {targetip} und PORT: {targetport}----------------------------\n")
        
        targetport = int(targetport)
        if targetip and targetport != 0:
            evaluate(targetip,targetport,proxy_list,counter,data_size) # Perform the TCP-Handshake with the proxy if there are still valid adresses in list
        else:
            break
    
    calc_score(proxy_list,input_handshake_tries)  
    print_proxy_list_dict(proxy_list) 



async def write_proxy_to_dict(input_number,proxies, proxy_list,input_handshake_tries):
        """"
        Query the Parameters to the dictionary --> TODO IMPL Object Orientated 
        """
        proxycount = 0
        while True:
            proxy = await proxies.get()
            if proxy is None:
                break
            
            ip = proxy.host
            port = proxy.port
            error_rate = proxy.error_rate
            avg_response_time = proxy.avg_resp_time
            
            #string = "{}".format(proxycount)
            
            proxy_list[proxycount]["ip"]=ip
            proxy_list[proxycount]["port"]=port
            proxy_list[proxycount]["handshakes"]= input_handshake_tries
            
            

            x = proxy_list[proxycount].items()
            print(f"FOUND PROXY:  {proxy.types}  and the actual proxy {x}\n")
            proxycount = proxycount + 1

def print_proxy_list_dict(proxy_list):
    """
    A function to print the actual proxy_list
    """

    print("\n \n ")
    print("   __________________________________________________________________________________________________________________________________________________________________")
    print("  |\n")
    for elements in proxy_list:
        index = proxy_list.index(elements)
        index += 1
        print(f"  > {index}. Proxy \n \n   {elements.items()}   \n")
    print("  |__________________________________________________________________________________________________________________________________________________________________\n")

    print("\n \n")            

def init_proxy_list(input_number,proxy_list):
    """
    A function to initialize a Proxy Object from the proxybroker queue and store it in a dict -> TODO IMPL OOP
    """
    for key in range(input_number):
        proxy_data = {"ip" : 0,
                    "port" :0,
                    "score" : 0,
                    "avg_syn_ack_time" : 0,
                    "avg_transmission_time" : 0,
                    "avg_throughput":0,
                    "handshakes" : 0,
                    "log_handshake": [],
                    "log_syn_ack_time" : [],
                    "log_transmission_time": [],
                    "log_throughput": []
                    
                    
                    
                    
                    }
        proxy_list.append(proxy_data)

def sort_proxy_list(proxy_list):
    """A Function for sorting the List and remove proxys with a 70 score threshold
    """
    #TODO SORT first, so that proxy with score 100 is on top
    
    proxy_list.sort(key=lambda e: e["score"], reverse=True)

    
    unbalanced = True
    
        
    #DELETE Proxys with score < 60
    while unbalanced and len(proxy_list) > 0:
        for elements in proxy_list:
            if elements["score"]<= 70:
                proxy_list.remove(elements)
                print("Removed Proxys with score < 70 \n")
                print_proxy_list_dict(proxy_list)
                sort_proxy_list(proxy_list)
            
            else: unbalanced = False

def refresh_proxy_list(Ready_for_connection: bool,proxy_list: list,proxy_list_slave:list):
        "A function for refilling the proxy list with new evaluated Proxys"
        if Ready_for_connection == False:
            if  len(proxy_list) <= 2 or proxy_list[0]["score"] < 130 or proxy_list[1]["score"] < 120: # and proxy_list[2]["score"] < 100 or proxy_list[0] == None:
                print("Refreshing the Proxy List \n")
                #asyncio.sleep(5)
                print("Refreshing the Proxy List \n")

                Ready_for_connection = False
                proxies = asyncio.Queue()
                broker = Broker(proxies)

            
                init_proxy_list(5, proxy_list_slave)

                tasks = asyncio.gather(broker.find( types=[ 'SOCKS5'],lvl = 'HIGH', strict = True,limit=5),
                            write_proxy_to_dict(5,proxies, proxy_list_slave,6),)
    
                loop = asyncio.get_event_loop()
                loop.run_until_complete(tasks)

                counter = 0
                evaluate_call(proxy_list_slave, counter,6,1000)
                sort_proxy_list(proxy_list_slave)
                for elements in proxy_list_slave:
                    if elements["score"] >= 100:
                        proxy_list.append(elements)
                        print("Proxy ATTACHED to MASTER List")
                
                sort_proxy_list(proxy_list)
                print_proxy_list_dict(proxy_list)

                if len(proxy_list) <= 2 and proxy_list[0]["score"] < 130 or proxy_list[1]["score"] < 120:
                    refresh_proxy_list(Ready_for_connection,proxy_list,proxy_list_slave)
                else:
                    Ready_for_connection = True
                    refresh_proxy_list(Ready_for_connection,proxy_list,proxy_list_slave)

            else:
                Ready_for_connection = True
                sort_proxy_list(proxy_list)
                print("Proxy List is ready for Connection")
        else:
                Ready_for_connection = True
                sort_proxy_list(proxy_list)
                print("Proxy List is ready for Connection")
                
def checker_proxy_list():
    "Perform an Evaluation Iteration on the Proxy List every 10 seconds"

def request(proxy_list):
    """
    url = ["https://ipinfo.io/ ,  "https://httpbin.org/#/Response_inspection"]

    ip = proxy_list[0]["ip"]

    proxy_for_connection = {
            "socks5": f"{ip}"
     }
    
    response = requests.get()

    """