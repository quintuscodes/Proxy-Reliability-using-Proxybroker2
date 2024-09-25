
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os 
import shutil
"Script for plotting the Project Proxy Manager Data."


def plot_avg_score_distribution(proxy_managers):
    data = []
    for manager in proxy_managers:
        protocol = manager.get_proto()
        for proxy in manager.get_master_list():
            data.append({'protocol': protocol, 'avg_score': proxy.avg_score})

    #Color
    pastel_colors = ['#AEC6CF', '#FFB7B2', '#B39EB5', '#FFDAC1']

    #Information
    info = 'Proxy_Num = 10, Eval_per_Iter = 10, Eval_Rounds = 6'
    # Convert to a DataFrame for easier plotting (requires pandas)
    
    df = pd.DataFrame(data)
    
    # Boxplot
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='protocol', y='avg_score', data=df,hue='protocol',palette=pastel_colors,legend=False)
    plt.title('Distribution of AVG_Scores by Protocol.')
    #plt.text(0.95,0.01, info,verticalalignment='bottom',horizontalalignment='right',
    #         transform=plt.gca().transAxes,color='gray',fontsize=12)
    plt.savefig('boxplot_avg_scores.png') # Save
    #plt.show()
    plt.close()
    #Clear Cache
    plt.clf()

    # Violinplot (alternative)
    plt.figure(figsize=(10, 6))
    sns.violinplot(x='protocol', y='avg_score', data=df,hue='protocol', palette=pastel_colors,legend=False)
    plt.title('Distribution of AVG_Scores by Protocol.')
    
    plt.savefig('violinplot_avg_scores.png') # Save
    plt.close()
    
    plt.clf()



def plot_top_proxies_by_protocol(proxy_managers, top_n=3):
    data = []
    pastel_colors = ['#AEC6CF', '#FFB7B2', '#B39EB5', '#FFDAC1', '#FFD700', '#66CDAA', '#FF69B4', '#8A2BE2', '#DC143C', '#00CED1']

    
    for manager in proxy_managers:
        protocol = manager.get_proto()
        sorted_proxies = sorted(manager.get_master_list(), key=lambda p: p.avg_score, reverse=True)
        for i in range(min(top_n, len(sorted_proxies))):
            proxy = sorted_proxies[i]
            data.append({
                'protocol': protocol, 
                'avg_score': proxy.avg_score, 
                'ip': proxy.get_ip()  
            })

    df = pd.DataFrame(data)

    
    plt.figure(figsize=(12, 6))
    
    
    sns.barplot(x='protocol', y='avg_score', hue='ip', data=df, palette=pastel_colors)

    plt.title(f'Top {top_n} Proxies by avg_score for each Protocol')

    

    
    handles, labels = plt.gca().get_legend_handles_labels()
    
  
    unique_labels = dict(zip(labels, handles))

    
    sorted_protocols = ['HTTP', 'SOCKS4', 'SOCKS5', 'CONNECT:25']
    sorted_labels = []

    for protocol in sorted_protocols:
        sorted_labels.extend([label for label in unique_labels if df[df['ip'] == label]['protocol'].iloc[0] == protocol])

    sorted_handles = [unique_labels[label] for label in sorted_labels]

    
    plt.legend(sorted_handles, sorted_labels, title='Grouped by Protocol', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.savefig('Top_Proxies_by_protocol.png')
    plt.close()
    plt.clf()



def filter_final_proxies(proxy_manager):
    
    
    final_proxies = set(proxy.get_ip() for proxy in proxy_manager.get_master_list())
    print(f"Final Proxies in Master List: {final_proxies}")

    
    filtered_data = []
    for epoch_data in proxy_manager.get_hist_data():  
        proxies = [proxy for proxy in epoch_data['proxies'] if proxy['ip'] in final_proxies]
        print(f"Epoch: {epoch_data['epoch']}, Filtered Proxies: {len(proxies)}, IPs: {[proxy['ip'] for proxy in proxies]}")
        filtered_data.append({'epoch': epoch_data['epoch'], 'proxies': proxies})

    return filtered_data

def plot_avg_throughput(proxy_manager_item):
    filtered_data = filter_final_proxies(proxy_manager_item)
    proto = proxy_manager_item.get_proto()
    
    unique_ips = set()
    for epoch_data in filtered_data:
        for proxy in epoch_data['proxies']:
            ip = proxy['ip']
            unique_ips.add(ip)

    
    color_map = plt.cm.get_cmap('tab20', len(unique_ips))
    ip_colors = {ip: color_map(i) for i, ip in enumerate(unique_ips)}

    
    plt.figure(figsize=(10, 6))

    for epoch_data in filtered_data:
        epoch = epoch_data['epoch']
        for proxy in epoch_data['proxies']:
            ip = proxy['ip']
            
            
            jittered_epoch = epoch + np.random.uniform(-0.2, 0.2)

            
            plt.scatter(jittered_epoch, proxy['avg_throughput'], color=ip_colors[ip])

    plt.xlabel('Epoch')
    plt.ylabel('Average Throughput in [KB/s]')
    plt.title(f'Average Throughput per Epoch of the {proto} - Protokoll ')

    plt.xticks(np.arange(1, 11, 1))
    handles = [plt.Line2D([0], [0], marker='o', color=ip_colors[ip], label=ip, linestyle='') for ip in unique_ips]
    plt.legend(handles=handles, title='IP Addresses', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.savefig('Plot_Avg_Throughput.png')
    plt.close()
    plt.clf()
def plot_avg_syn_ack_time(proxy_manager_item):

    
    filtered_data = filter_final_proxies(proxy_manager_item)
    proto = proxy_manager_item.get_proto()

    
    unique_ips = set()
    for epoch_data in filtered_data:
        for proxy in epoch_data['proxies']:
            ip = proxy['ip']
            unique_ips.add(ip)

    
    color_map = plt.cm.get_cmap('tab20', len(unique_ips))
    ip_colors = {ip: color_map(i) for i, ip in enumerate(unique_ips)}

    
    plt.figure(figsize=(10, 6))

    for epoch_data in filtered_data:
        epoch = epoch_data['epoch']
        for proxy in epoch_data['proxies']:
            ip = proxy['ip']
            
            
            jittered_epoch = epoch + np.random.uniform(-0.1, 0.1)

            
            plt.scatter(jittered_epoch, proxy['avg_syn_ack_time'], color=ip_colors[ip])

    plt.xlabel('Epoch')
    plt.ylabel('Average SYN-ACK Time in [s]')
    plt.title(f'Average SYN-ACK Time per Epoch of the {proto} - Protokoll')

    
    plt.xticks(np.arange(1, 11, 1))  # Setzt die Ticks auf die Werte 1 bis 10

    
    plt.ylim(0, 1)

    
    handles = [plt.Line2D([0], [0], marker='o', color=ip_colors[ip], label=ip, linestyle='') for ip in unique_ips]
    plt.legend(handles=handles, title='IP Addresses', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.savefig('Plot_Avg_SYN_ACK_Time.png')
    plt.close()
    plt.clf()

def plot_avg_transmission_time(proxy_manager_item):
    filtered_data = filter_final_proxies(proxy_manager_item)
    proto = proxy_manager_item.get_proto()
    unique_ips = set()
    for epoch_data in filtered_data:
        for proxy in epoch_data['proxies']:
            ip = proxy['ip']
            unique_ips.add(ip)

    
    color_map = plt.cm.get_cmap('tab20', len(unique_ips))
    ip_colors = {ip: color_map(i) for i, ip in enumerate(unique_ips)}

    
    plt.figure(figsize=(10, 6))

    for epoch_data in filtered_data:
        epoch = epoch_data['epoch']
        for proxy in epoch_data['proxies']:
            ip = proxy['ip']
            
            
            jittered_epoch = epoch + np.random.uniform(-0.2, 0.2)

            
            plt.scatter(jittered_epoch, proxy['avg_transmission_time'], color=ip_colors[ip])

    plt.xlabel('Epoch')
    plt.ylabel('Average Transmission Time in [s]')
    plt.title(f'Average Transmission Time per Epoch of the {proto} - Protokoll')
    plt.xticks(np.arange(1, 11, 1))
    
    handles = [plt.Line2D([0], [0], marker='o', color=ip_colors[ip], label=ip, linestyle='') for ip in unique_ips]
    plt.legend(handles=handles, title='IP Addresses', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.savefig('Plot_Avg_Transmission_Time.png')
    plt.close()
    plt.clf()

def plot_HR_and_RR(proxy_manager_item):
    filtered_data = filter_final_proxies(proxy_manager_item)
    proto = proxy_manager_item.get_proto()
    "Plot Handshake and Request Rate"
    unique_ips = set()
    for epoch_data in filtered_data:
        for proxy in epoch_data['proxies']:
            ip = proxy['ip']
            unique_ips.add(ip)

    
    color_map = plt.cm.get_cmap('tab20', len(unique_ips))
    ip_colors = {ip: color_map(i) for i, ip in enumerate(unique_ips)}

    
    plt.figure(figsize=(10, 6))

    for epoch_data in filtered_data:
        epoch = epoch_data['epoch']
        for proxy in epoch_data['proxies']:
            ip = proxy['ip']
            
            
            jittered_epoch = epoch + np.random.uniform(-0.2, 0.2)

            
            plt.scatter(jittered_epoch, proxy['handshake_rate'], color=ip_colors[ip], marker='o')

            
            plt.scatter(jittered_epoch, proxy['request_rate'], color=ip_colors[ip], marker='x')

    plt.xlabel('Epoch')
    plt.ylabel('Rate Values in [%]')
    plt.title(f'Handshake Rate (HR) and Request Rate (RR) per Epoch of the {proto} - Protokoll ')
    plt.xticks(np.arange(1, 11, 1))
    
    handles = []
    for ip in unique_ips:
        hr_handle = plt.Line2D([0], [0], marker='o', color=ip_colors[ip], label=f'{ip} HR', linestyle='')  # Kreis für HR
        rr_handle = plt.Line2D([0], [0], marker='x', color=ip_colors[ip], label=f'{ip} RR', linestyle='')  # X für RR
        handles.extend([hr_handle, rr_handle])

    plt.legend(handles=handles, title='IP Addresses', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.savefig('Plot_Handshake_and_Request_Rate.png')
    plt.close()
    plt.clf()

def move_plots(run_number, proxy_num, eval_rounds):
    
    folder_name = f"Lauf_{run_number}_proxy_num={proxy_num}_eval_rounds={eval_rounds}"
    
    
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

   
    plot_files = [
        'violinplot_avg_scores.png',
        'Top_Proxies_by_protocol.png',
        'Plot_Avg_Throughput.png',
        'Plot_Avg_Transmission_Time.png',
        'Plot_Avg_SYN_ACK_Time.png',
        'Plot_Handshake_and_Request_Rate.png',
        'boxplot_avg_scores.png'
    ]
    #Move
    
    for plot in plot_files:
        if os.path.exists(plot):  
            shutil.move(plot, os.path.join(folder_name, plot))
        else:
            print(f"Plot {plot} wurde nicht gefunden.")