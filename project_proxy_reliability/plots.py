"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

"Script for plotting the Project Proxy Manager Data."


def plot_avg_score_distribution(proxy_managers):
    data = []
    for manager in proxy_managers:
        protocol = manager.protocol
        for proxy in manager.get_proxy_list():
            data.append({'protocol': protocol, 'avg_score': proxy.avg_score})

    # Convert to a DataFrame for easier plotting (requires pandas)
    
    df = pd.DataFrame(data)

    # Boxplot
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='protocol', y='avg_score', data=df)
    plt.title('Distribution of avg_scores by Protocol')
    plt.show()

    Violinplot (alternative)
    plt.figure(figsize=(10, 6))
    sns.violinplot(x='protocol', y='avg_score', data=df)
    plt.title('Distribution of avg_scores by Protocol')
    plt.show()
    """
    