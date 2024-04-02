"""Find and show 10 working SOCKS5 proxies perform a TCP Handshake individually."""

from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.inet import TCP
import asyncio
from proxybroker import Broker, Proxy

def handshake(ip, port, proxy_list,counter):
    print(f"#################################################### {counter} . RUNDE ###########################################################")
# Target IP and Port Adress from gathered Proxy List
    target_ip = ip
    target_port = port

# Create SYN-Paket to Proxy
    syn_packet = IP(dst=target_ip) / TCP(dport=target_port, flags="S")

# Transceive SYN-Paket and Receive Answer
    syn_ack_response = sr1(syn_packet, timeout=2, verbose=False)

    if syn_ack_response:
        if syn_ack_response.haslayer(TCP) and syn_ack_response[TCP].flags & 0x12:
            print("SYN-ACK empfangen. Handshake erfolgreich.")
        # Create ACK-Paket to Proxy
            ack_packet = IP(dst=target_ip) / TCP(dport=target_port, flags="A",
                                              seq=syn_ack_response[TCP].ack,
                                              ack=syn_ack_response[TCP].seq + 1)
        # Send ACK-Paket to Proxy
            send(ack_packet)
            print("ACK gesendet. Handshake abgeschlossen.")
            
            for elements in proxy_list:
                if elements.get("ip") == target_ip and elements.get("port") == target_port:
                    
                    elements["log_handshake"].append(1)#log successful handshake
                    x = elements.get("log_handshake")
                    print(f"Log Handshake set to {x}")
        else:
            print("SYN-ACK nicht empfangen. Handshake fehlgeschlagen.")
            
            for elements in proxy_list:
                if elements.get("ip") == target_ip and elements.get("port") == target_port:
                    
                    elements["log_handshake"].append(0)#log unsuccessful handshake
                    x = elements.get("log_handshake")
                    print(f"Log Handshake set to {x}")
            
    else:
        print("Keine Antwort empfangen. Handshake fehlgeschlagen.")
        
        for elements in proxy_list:
            if elements.get("ip") == target_ip and elements.get("port") == target_port:
                    
                    elements["log_handshake"].append(0)#log unsuccessful handshake
                    x = elements.get("log_handshake")
                    print(f"Log Handshake set to {x}")

def calc_score(proxy_list,input_handshake_tries):
    #Calculate TCP-Handshake Score
    for elements in proxy_list:
        succ_handshakes = elements["log_handshake"].count(1)
        handshake_rate = succ_handshakes / input_handshake_tries
        score = handshake_rate * 100
        elements["score"]= score
    #Add Bonus of 3 Best Avg_resp_time to score ; 15 , 10 , 5 points
        
    """
    proxy_list_copy = proxy_list
    ranked_list = []
    
    for i in range(0,2):
        max_global= 1
        best_proxy = 0
        for elements in proxy_list_copy:
            max_local = elements.get("avg_resp_time")
            if max_local < max_global:
                ranked_list.append(elements)
                proxy_list_copy.remove(elements)
                max_global = max_local
            else:
                max_global = max_local
    """

def handshake_call(proxy_list,counter, input_handshake_tries):
  while counter < input_handshake_tries: 
    counter += 1 
    for elements in proxy_list:
        
        targetip =  elements["ip"]
        targetport = elements["port"]
        
        print(f"------------------------------Handshake fuer neuen Proxy mit IP: {targetip} und PORT: {targetport}----------------------------")
        
        targetport = int(targetport)
        handshake(targetip,targetport,proxy_list,counter) # Perform the TCP-Handshake with the proxy.
        
    #TODO is_proxy_working mit Score anpassen
    calc_score(proxy_list,input_handshake_tries)  
    print_proxy_list_dict(proxy_list) 



async def write_proxy_to_dict(input_number,proxies, proxy_list):
        proxycount = 0
        while True:
            proxy = await proxies.get()
            if proxy is None:
                break
            
            ip = proxy.host
            port = proxy.port
            error_rate = proxy.error_rate
            avg_response_time = proxy.avg_resp_time
            is_working = proxy.is_working
            #string = "{}".format(proxycount)
            
            proxy_list[proxycount]["ip"]=ip
            proxy_list[proxycount]["port"]=port
            proxy_list[proxycount]["error_rate"]=error_rate
            proxy_list[proxycount]["avg_resp_time"]=avg_response_time
            proxy_list[proxycount]["is_proxy_working"]=is_working

            x = proxy_list[proxycount].items()
            print(f"FOUND PROXY:  {proxy.types}  and the actual proxy {x}")
            proxycount = proxycount + 1

def print_proxy_list_dict(proxy_list):
    for elements in proxy_list:
        print(elements.items())          

def init_proxy_list(input_number,proxy_list):
    for key in range(input_number):
        proxy_data = {"ip" : 0,
                    "port" :0,
                    "score" : 0,
                    "is_proxy_working": False,
                    "error_rate" : 0,
                    "avg_resp_time" : 0,
                    "log_handshake": []
                    }
        proxy_list.append(proxy_data)

