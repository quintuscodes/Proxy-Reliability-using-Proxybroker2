"""Find and show 10 working SOCKS5 proxies and evaluate them individually."""

from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.inet import TCP
import asyncio
from proxybroker import Broker, Proxy

def handshake(ip, port, proxy_list,counter,data_size):
    print(f"#################################################### {counter} . RUNDE ###########################################################")
# Target IP and Port Adress from gathered Proxy List
    target_ip = ip
    target_port = port

# Create SYN-Paket to Proxy
    syn_packet = IP(dst=target_ip) / TCP(dport=target_port, flags="S")
    print("Erstelle SYN- Paket: \n")
    #syn_packet.show()

    #Data Packet for Measuring Transmission Time of 64Bytes of data
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

    
    print("Vor SYN ACK Sortierung \n")
    print_proxy_list_dict(proxy_list)
    

    proxy_list.sort(key=lambda e: e["avg_syn_ack_time"], reverse=False) 
    print("Nach AVG SYN-ACK Sortierung\n")
    print_proxy_list_dict(proxy_list)
    proxy_list[0]["score"] += 15
    proxy_list[1]["score"] += 10
    proxy_list[2]["score"] += 5
    print("Nach SYN ACK Score Anpassung\n")
    print_proxy_list_dict(proxy_list)
        
    #TODO Transmission Time Score calculation
    proxy_list.sort(key=lambda e: e["avg_transmission_time"], reverse=False)
    print("Nach AVG Transmission Time Sortierung\n")
    print_proxy_list_dict(proxy_list)
    proxy_list[0]["score"] += 15
    proxy_list[1]["score"] += 10
    proxy_list[2]["score"] += 5
    print("Nach AVG Transmission Time Score Anpassung\n")
    print_proxy_list_dict(proxy_list)
    print("Nach Score Sortierung\n")
    proxy_list.sort(key=lambda e: e["score"], reverse=True)
    print_proxy_list_dict(proxy_list)

    #TODO AVG Throughput Score calculation


def handshake_call(proxy_list,counter, input_handshake_tries,data_size):
  while counter < input_handshake_tries: 
    counter += 1 
    for elements in proxy_list:
        
        targetip =  elements["ip"]
        targetport = elements["port"]
        
        print(f"------------------------------Handshake fuer neuen Proxy mit IP: {targetip} und PORT: {targetport}----------------------------\n")
        
        targetport = int(targetport)
        handshake(targetip,targetport,proxy_list,counter,data_size) # Perform the TCP-Handshake with the proxy.
        
    
    calc_score(proxy_list,input_handshake_tries)  
    print_proxy_list_dict(proxy_list) 



async def write_proxy_to_dict(input_number,proxies, proxy_list,input_handshake_tries):
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
    # SORT List given the "score"-Field if a Proxy with score 100 is already available else --> FIND
    #TODO SORT first that proxy with score 100 is on top
    
    proxy_list.sort(key=lambda e: e["score"], reverse=True)

    
    unbalanced = True
    #if proxy_list[0]["score"] == 100:
        
        #DELETE Proxys with score < 60
        #TODO Still deletes not all proxys from list
    while unbalanced:
        for elements in proxy_list:
            if elements["score"] <= 50:
                proxy_list.remove(elements)
                print("Removed Proxys with score < 60 \n")
                print_proxy_list_dict(proxy_list)
                sort_proxy_list(proxy_list)
            
            else: unbalanced = False
             
        #[proxy_list.remove(elements) for elements in proxy_list if elements["score"] <= 60]
        # FIND 3 new Proxys with score = 100
    
    print("Nach Sortierung:\n")

    print_proxy_list_dict(proxy_list)



def refresh_proxy_list(Ready_for_connection: bool,proxy_list: list,proxy_list_slave:list):
        "A function for refilling the proxy list with new evaluated Proxys"
        
        if  proxy_list[0]["score"] < 100 and proxy_list[1]["score"] < 100 and proxy_list[2]["score"] < 100 or proxy_list[0] == None:
            print("Refreshing the Proxy List \n")
            asyncio.sleep(5)
            print("Refreshing the Proxy List \n")

            Ready_for_connection = False
            proxies = asyncio.Queue()
            broker = Broker(proxies)

            
            init_proxy_list(5, proxy_list_slave)
            broker.find( types=[ 'SOCKS5'],lvl = 'HIGH', strict = True,limit=5)
            write_proxy_to_dict(5,proxies, proxy_list_slave,6)
            counter = 0
            handshake_call(proxy_list, counter,5,1000)
            sort_proxy_list(proxy_list_slave)
            for elements in proxy_list_slave:
                if elements["score"] >= 100:
                    proxy_list.append(elements)
                    print("Proxy ATTACHED to MASTER List")
            
            refresh_proxy_list(Ready_for_connection,proxy_list,proxy_list_slave)

        else:
            Ready_for_connection = True
            print("Proxy List is ready for Connection")

def checker_proxy_list():
    "Perform an Evaluation Iteration on the Proxy List every 10 seconds"

            
            