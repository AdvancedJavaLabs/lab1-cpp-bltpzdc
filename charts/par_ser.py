import matplotlib.pyplot as plt
import re

def plot_serial_vs_parallel_lines(data):
    meaningful_data = {}
    for problem, times in data.items():
        if times['serial_times'][0] > 0 or times['parallel_times'][0] > 0:
            meaningful_data[problem] = times
    
    problems = list(meaningful_data.keys())
    serial_times = [meaningful_data[p]['serial_times'][0] for p in problems]
    parallel_times = [meaningful_data[p]['parallel_times'][0] for p in problems]
    
    plt.figure(figsize=(12, 8))
    
    vertices = []
    for problem in problems:
        match = re.search(r'(\d+\.?\d*)\s*[KM]?\s*vertices', problem)
        if match:
            num = float(match.group(1))
            if 'M' in problem:
                vertices.append(int(num * 1000000))
            elif 'K' in problem:
                vertices.append(int(num * 1000))
            else:
                vertices.append(int(num))
    
    plt.plot(problems, serial_times, 'ro-', linewidth=3, markersize=10, label='Serial BFS', markerfacecolor='red')
    plt.plot(problems, parallel_times, 'bo-', linewidth=3, markersize=10, label='Parallel BFS (12 threads)', markerfacecolor='blue')
    
    plt.ylabel('Execution Time (ms)', fontsize=12)
    plt.title('Serial vs Parallel BFS Execution Time', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    
    for i, (s, p) in enumerate(zip(serial_times, parallel_times)):
        if s > 0:
            plt.annotate(f'{s}ms', (i, s), textcoords="offset points", 
                        xytext=(0,15), ha='center', fontsize=9, color='red', fontweight='bold')
        if p > 0:
            plt.annotate(f'{p}ms', (i, p), textcoords="offset points", 
                        xytext=(0,-20), ha='center', fontsize=9, color='blue', fontweight='bold')
    
    plt.tight_layout()
    plt.show()

bfs_data = {
    '10 vertices, 50 connections': {
        'serial_times': [0],
        'parallel_times': [1]
    },
    '100 vertices, 500 connections': {
        'serial_times': [0],
        'parallel_times': [0]
    },
    '1K vertices, 5K connections': {
        'serial_times': [0],
        'parallel_times': [0]
    },
    '10K vertices, 50K connections': {
        'serial_times': [0],
        'parallel_times': [1]
    },
    '10K vertices, 100K connections': {
        'serial_times': [0],
        'parallel_times': [0]
    },
    '50K vertices, 1M connections': {
        'serial_times': [6],
        'parallel_times': [4]
    },
    '100K vertices, 1M connections': {
        'serial_times': [11],
        'parallel_times': [6]
    },
    '1M vertices, 10M connections': {
        'serial_times': [144],
        'parallel_times': [60]
    },
    '2M vertices, 10M connections': {
        'serial_times': [220],
        'parallel_times': [123]
    },
    '20M vertices, 50M connections': {
        'serial_times': [2761],
        'parallel_times': [1599]
    }
}

plot_serial_vs_parallel_lines(bfs_data)