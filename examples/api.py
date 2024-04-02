"""Find and show 10 working SOCKS5 proxies and perform a TCP Handshake individually."""

from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.inet import TCP
import asyncio
from proxybroker import Broker, Proxy

def handshake(ip, port, proxy_list,counter):
    print(f"#################################################### {counter} . RUNDE ###########################################################")
# Ziel-IP-Adresse und Port des Proxy Servers
    target_ip = ip
    target_port = port

# Erstellen des SYN-Pakets an Proxy
    syn_packet = IP(dst=target_ip) / TCP(dport=target_port, flags="S")

# Senden des SYN-Pakets und Empfangen der Antwort an/von Proxy
    syn_ack_response = sr1(syn_packet, timeout=2, verbose=False)

    if syn_ack_response:
        if syn_ack_response.haslayer(TCP) and syn_ack_response[TCP].flags & 0x12:
            print("SYN-ACK empfangen. Handshake erfolgreich.")
        # Erstellen des ACK-Pakets für den abschließenden Teil des Handshakes
            ack_packet = IP(dst=target_ip) / TCP(dport=target_port, flags="A",
                                              seq=syn_ack_response[TCP].ack,
                                              ack=syn_ack_response[TCP].seq + 1)
        # Senden des ACK-Pakets
            send(ack_packet)
            print("ACK gesendet. Handshake abgeschlossen.")
            
            for elements in proxy_list:
                if elements.get("ip") == target_ip and elements.get("port") == target_port:
                    elements["score"]= 100
                    x = elements.get("score")
                    print(f"Score set to {x}")
        else:
            print("SYN-ACK nicht empfangen. Handshake fehlgeschlagen.")
            
            for elements in proxy_list:
                if elements.get("ip") == target_ip and elements.get("port") == target_port:
                    elements["score"]= 0
                    x = elements.get("score")
                    print(f"Score set to {x}")
            
    else:
        print("Keine Antwort empfangen. Handshake fehlgeschlagen.")
        
        for elements in proxy_list:
            if elements.get("ip") == target_ip and elements.get("port") == target_port:
                    elements["score"]= 0
                    x = elements.get("score")
                    print(f"Score set to {x}")


def handshake_call(proxy_list,counter, handshake_tries):
  while counter < handshake_tries: 
    counter += 1 
    for elements in proxy_list:
        
        targetip =  elements["ip"]
        targetport = elements["port"]
        
        print(f"------------------------------Handshake fuer neuen Proxy mit IP: {targetip} und PORT: {targetport}----------------------------")
        
        targetport = int(targetport)
        handshake(targetip,targetport,proxy_list,counter)
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
                    }
        proxy_list.append(proxy_data)

