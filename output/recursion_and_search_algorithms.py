import networkx as nx

# Recursion Problem: Factorial
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

# Depth-First Search (DFS) Problem: Traverse a Graph
def dfs(graph, start):
    visited = set()
    traversal_order = []
    stack = [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            traversal_order.append(vertex)
            for neighbor in graph[vertex]:
                stack.append(neighbor)
    return traversal_order

# Breadth-First Search (BFS) Problem: Traverse a Graph
def bfs(graph, start):
    visited = set()
    traversal_order = []
    queue = [start]
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            traversal_order.append(vertex)
            for neighbor in graph[vertex]:
                queue.append(neighbor)
    return traversal_order

# Merge Sort Algorithm
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]
    return merge(merge_sort(left_half), merge_sort(right_half))

def merge(left, right):
    merged = []
    left_index = 0
    right_index = 0
    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1
    merged += left[left_index:]
    merged += right[right_index:]
    return merged

# Example usage:
g = {1: [2, 3], 2: [1, 4], 3: [1, 4], 4: [2, 3]}
print(dfs(g, 1))
print(bfs(g, 1))
print(merge_sort([38, 27, 43, 3, 9, 82, 10]))