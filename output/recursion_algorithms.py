import collections

# Breadth-First Search (BFS)

def bfs(graph, root):
    visited = set()
    queue = collections.deque([root])
    while queue:
        vertex = queue.popleft()
        print(vertex, end=' ') # process the vertex
        for neighbour in graph[vertex]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)

# Depth-First Search (DFS)

def dfs(graph, root):
    visited = set()
    def dfs_helper(vertex):
        visited.add(vertex)
        print(vertex, end=' ') # process the vertex
        for neighbour in graph[vertex]:
            if neighbour not in visited:
                dfs_helper(neighbour)
    dfs_helper(root)

# Famous Recursion Problems and Solutions

# 1. Factorial

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

# 2. Fibonacci Series

def fibonacci(n):
    if n <= 0:
        return "Input should be positive integer"
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n):
            a, b = b, a+b
        return b

# 3. Binary Search

def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

# 4. Merge Sort

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])
    return merge(left_half, right_half)

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

# 5. Quick Sort

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# 6. Tower of Hanoi

def tower_of_hanoi(n, from_rod, to_rod, aux_rod):
    if n == 1:
        print(f"Move disk 1 from rod {from_rod} to rod {to_rod}")
        return
    tower_of_hanoi(n - 1, from_rod, aux_rod, to_rod)
    print(f"Move disk {n} from rod {from_rod} to rod {to_rod}")
    tower_of_hanoi(n - 1, aux_rod, to_rod, from_rod)

# 7. Fibonacci Series using Recursion

def fibonacci_recursive(n):
    if n <= 1:
        return n
    else:
        return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

# 8. Binary Search using Recursion

def binary_search_recursive(arr, target, low, high):
    if low > high:
        return -1
    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, high)
    else:
        return binary_search_recursive(arr, target, low, mid - 1)

# 9. Merge Sort using Recursion

def merge_sort_recursive(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left_half = merge_sort_recursive(arr[:mid])
    right_half = merge_sort_recursive(arr[mid:])
    return merge_recursive(left_half, right_half)

def merge_recursive(left, right):
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

# 10. Quick Sort using Recursion

def quick_sort_recursive(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort_recursive(left) + middle + quick_sort_recursive(right)
