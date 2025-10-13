#pragma once

#include <condition_variable>
#include <queue>

using batch = std::vector<int>;
struct SynchronizedQueue {
    std::mutex mutex;
    std::condition_variable cv;
    std::queue<batch> queue;

    size_t idle {};
    bool done {};
};

class Graph {
public:
    explicit Graph(int vertices);
    void addEdge(int src, int dest);
    void parallelBFS(int startVertex); // заглушка, как в Java
    void bfs(int startVertex);         // обычный BFS
    int vertices() const;

private:
    int V;
    std::vector<std::vector<int>> adjList;
};