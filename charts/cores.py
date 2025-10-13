import matplotlib.pyplot as plt

def plot_multi_problem_thread_scaling(data_dict):
    fig, (ax1) = plt.subplots(1, 1, figsize=(18, 5))
    
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'black', 'pink', 'purple', 'brown', 'olive']
    for i, (problem_name, data) in enumerate(data_dict.items()):
        threads = data['threads']
        times = data['times']
        
        ax1.plot(threads, times, 
                color=colors[i], linewidth=2, 
                markersize=8, label=problem_name)
        
        ax1.annotate(problem_name.split(' ')[0], 
                    xy=(threads[-1], times[-1]),
                    xytext=(10, 0), textcoords='offset points',
                    fontsize=9, alpha=0.8)
    
    ax1.set_xlabel('Number of Threads')
    ax1.set_ylabel('Execution Time (ms)')
    ax1.set_title('Execution Time vs Thread Count')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax1.grid(True, alpha=0.3)
    
    plt.show()


sample_data = {
    '10 vertices, 50 connections': {
        'threads': [2, 4, 6, 8, 10, 12],
        'times': [0, 0, 0, 0, 1, 1]
    },
    '100 vertices, 500 connections': {
        'threads': [2, 4, 6, 8, 10, 12],
        'times': [0, 0, 0, 0, 0, 0]
    },
    '1000 vertices, 5000 connections': {
        'threads': [2, 4, 6, 8, 10, 12],
        'times': [0, 0, 0, 0, 0, 0]
    },
    '10000 vertices, 50000 connections': {
        'threads': [2, 4, 6, 8, 10, 12],
        'times': [0, 0, 0, 0, 0, 1]
    },
    '10000 vertices, 100000 connections': {
        'threads': [2, 4, 6, 8, 10, 12],
        'times': [1, 1, 1, 1, 0, 0]
    },
    '50K vertices, 1M connections': {
        'threads': [2, 4, 6, 8, 10, 12],
        'times': [17, 7, 6, 5, 4, 4]
    },
    '100K vertices, 1M connections': {
        'threads': [2, 4, 6, 8, 10, 12],
        'times': [23, 11, 9, 9, 7, 6]
    },
    '1M vertices, 10M connections': {
        'threads': [2, 4, 6, 8, 10, 12],
        'times': [198, 106, 86, 75, 63, 60]
    },
    '2M vertices, 10M connections': {
        'threads': [2, 4, 6, 8, 10, 12],
        'times': [342, 199, 167, 129, 122, 123]
    },
    '20M vertices, 50M connections': {
        'threads': [2, 4, 6, 8, 10, 12],
        'times': [3558, 2529, 1664, 1726, 1617, 1599]
    }
}

plot_multi_problem_thread_scaling(sample_data)