#include "Graph.h"
#include <algorithm>

Graph::Graph(int vertices) : V(vertices), adjList(vertices) {}

void Graph::addEdge(int src, int dest) {
    if (src < 0 || dest < 0 || src >= V || dest >= V) return;
    auto& vec = adjList[src];
    if (std::find(vec.begin(), vec.end(), dest) == vec.end()) {
        vec.push_back(dest);
    }
}

void Graph::parallelBFS(int startVertex) {

    if (startVertex < 0 or startVertex >= V) return;

#ifdef __unsafe
    std::vector<int> levels(V);
#else
    std::vector<std::atomic<int>> levels(V);
#endif
    for ( auto& lvl : levels ) { lvl = -1; }
    levels[startVertex] = 0;

    SynchronizedQueue q;
    q.queue.push(batch {startVertex});

    auto workers_count = std::thread::hardware_concurrency();
    if ( not workers_count ) { workers_count = 4; }
    std::vector<std::thread> workers;

    auto pop_batch = [&]() -> batch {
        std::unique_lock lk{q.mutex};
        if ( ++q.idle == workers_count and q.queue.empty() ) {
            q.done = true;
            q.cv.notify_all();
            return batch {};
        }
        q.cv.wait(lk, [&q]() { return not q.queue.empty() or q.done; });
        if ( q.done ) { return batch {}; }

        auto res = std::move(q.queue.front());
        q.queue.pop();
        --q.idle;
        return res;
    };

    auto process_batch = [&](const batch& b) -> void {
        std::vector<batch> processed;
        auto cur_batch = &processed.emplace_back();

        for ( const auto elt : b ) {
#ifdef __unsafe
            auto cur_level = levels[elt] + 1;
#else
            auto cur_level = levels[elt].load() + 1;
#endif
            for ( const auto neigh : adjList[elt] ) {
#ifdef __unsafe
                if ( auto& level = levels[neigh]; level == -1 or level > cur_level ) {
                    level = cur_level;
                    cur_batch->emplace_back(neigh);
                }
#else
                int expected = -1;
                if ( levels[neigh].compare_exchange_weak(expected, cur_level) ) {
                    cur_batch->emplace_back(neigh);
                } else {
                    expected = levels[neigh].load();
                    while ( expected > cur_level ) {
                        if ( levels[neigh].compare_exchange_weak(expected, cur_level) ) {
                            cur_batch->emplace_back(neigh);
                            break;
                        }
                        expected = levels[neigh].load();
                    }
                }
#endif

                if ( cur_batch->size() >= 256 ) {
                    cur_batch = &processed.emplace_back();
                }
            }
        }

        for ( auto& nb : processed ) {
            if ( nb.size() ) {
                {
                    std::unique_lock lk{q.mutex};
                    q.queue.push(std::move(nb));
                }
                q.cv.notify_one();
            }
            
        }
    };

    auto thread_func = [&pop_batch, &process_batch]() -> void {
        batch b = pop_batch();
        while ( not b.empty() ) {
            process_batch(b);
            b = pop_batch();
        }
    };

    for ( size_t i = 0; i < workers_count; ++i ) {
        workers.emplace_back(thread_func);
    }

    while ( workers_count ) {
        if ( auto& worker = workers[workers_count - 1]; worker.joinable() ) {
            worker.join();
            --workers_count;
        }
    }

}

void Graph::bfs(int startVertex) {
    if (startVertex < 0 || startVertex >= V) return;
    std::vector<char> visited(V, 0);
    std::queue<int> q;

    visited[startVertex] = 1;
    q.push(startVertex);

    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (int n : adjList[u]) {
            if (!visited[n]) {
                visited[n] = 1;
                q.push(n);
            }
        }
    }
}

int Graph::vertices() const { return V; }