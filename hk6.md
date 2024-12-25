# P（Polynomial time）

是指可以在多項式時間內找到解的問題集合。

如 **最短路徑問題**

```
import heapq

def dijkstra(graph, start, end):
    pq = []  # 優先佇列
    heapq.heappush(pq, (0, start))  # (距離, 節點)
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_node == end:
            return current_distance

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    return float('inf')  # 若無法到達終點

# 測試圖
graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('C', 2), ('D', 6)],
    'C': [('D', 3)],
    'D': []
}
print("Shortest path from A to D:", dijkstra(graph, 'A', 'D'))

```

# NP（Nondeterministic Polynomial time）

是指可以在多項式時間內驗證解是否正確的問題集合。

如 **子集和問題**

```
def subset_sum(nums, target):
    def dfs(index, current_sum):
        if current_sum == target:
            return True
        if index == len(nums) or current_sum > target:
            return False
        return dfs(index + 1, current_sum + nums[index]) or dfs(index + 1, current_sum)

    return dfs(0, 0)

# 測試
nums = [3, 34, 4, 12, 5, 2]
target = 9
print("Subset sum exists:", subset_sum(nums, target))

```

# NP-Complete（NP 完全問題）

是指最難的 NP 問題，解決它們意味著解決所有 NP 問題。

如 **旅行推銷員問題（TSP）**

```
from itertools import permutations

def tsp_brute_force(graph, start):
    nodes = list(graph.keys())
    nodes.remove(start)
    min_cost = float('inf')
    best_path = []

    for perm in permutations(nodes):
        current_path = [start] + list(perm) + [start]
        current_cost = sum(graph[current_path[i]][current_path[i + 1]] for i in range(len(current_path) - 1))
        if current_cost < min_cost:
            min_cost = current_cost
            best_path = current_path

    return min_cost, best_path

# 測試圖
graph = {
    'A': {'B': 10, 'C': 15, 'D': 20},
    'B': {'A': 10, 'C': 35, 'D': 25},
    'C': {'A': 15, 'B': 35, 'D': 30},
    'D': {'A': 20, 'B': 25, 'C': 30}
}
print("TSP solution:", tsp_brute_force(graph, 'A'))

```

# P vs NP 問題

是問是否所有能快速驗證答案的問題也能快速找到答案（即 P 是否等於 NP）。

如 **密碼學**，許多加密方法（如 RSA）依賴於 NP 問題的計算困難，例如分解大數為質因數，雖然驗證乘積是否正確很快，但找到分解卻非常困難。