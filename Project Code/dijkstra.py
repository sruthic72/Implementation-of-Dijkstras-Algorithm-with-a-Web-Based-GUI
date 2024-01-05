import heapq

def bellman_ford(graph, start):
    # Initialize distances
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    # Relax edges V-1 times
    for _ in range(len(graph) - 1):
        for node in graph:
            for neighbor, weight in graph[node].items():
                if distances[node] + weight < distances[neighbor]:
                    distances[neighbor] = distances[node] + weight

    # Check for negative cycles on the V-th iteration
    for node in graph:
        for neighbor, weight in graph[node].items():
            if distances[node] + weight < distances[neighbor]:
                return True  # Negative cycle detected

    return False

def dijkstra(graph, start, end):
    if start not in graph or end not in graph:
        print(f"Either {start} or {end} is not in the graph.")
        return []

    # Check for negative cycles
    if bellman_ford(graph, start):
        print("Negative cycle detected.")
        return []

    shortest_path = {node: float('inf') for node in graph}
    shortest_path[start] = 0
    previous_nodes = {node: None for node in graph}

    print(f"Initial shortest paths: {shortest_path}")
    print(f"Initial previous nodes: {previous_nodes}")

    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # If this distance has already been processed, skip
        if current_distance > shortest_path[current_node]:
            continue

        for neighbor, distance in graph[current_node].items():
            distance_through_current = distance + current_distance
            if distance_through_current < shortest_path[neighbor]:
                shortest_path[neighbor] = distance_through_current
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance_through_current, neighbor))

        print(f"Shortest paths after processing node {current_node}: {shortest_path}")
        print(f"Previous nodes after processing node {current_node}: {previous_nodes}")

    # Reconstruct path
    path = []
    while end:
        if end not in previous_nodes:
            print(f"Node {end} not in previous nodes. Unable to reconstruct full path.")
            return []

        path.append(end)
        end = previous_nodes[end]

    # Ensure the path is valid
    if path and path[-1] == start:
        print(f"Reconstructed path: {path[::-1]}")
        return path[::-1]
    else:
        print(f"No path found from {start} to {end}.")
        return []


def test_dijkstra(graph, start_node, end_node, expected_path):
    print(f"\nTesting path from {start_node} to {end_node} in graph: {graph}")
    path = dijkstra(graph, start_node, end_node)
    print(f"Expected: {expected_path}")
    print(f"Got: {path}")
    print("----" * 10)

if __name__ == "__main__":
    # 1. Basic Graph
    graph1 = {
        'A': {'B': 2, 'C': 4},
        'B': {'A': 2, 'C': 1, 'D': 5},
        'C': {'A': 4, 'B': 1, 'D': 3},
        'D': {'B': 5, 'C': 3}
    }
    test_dijkstra(graph1, 'A', 'D', ['A', 'B', 'C', 'D'])
    test_dijkstra(graph1, 'D', 'A', ['D', 'C', 'B', 'A'])
    
    # 2. Disconnected Graph
    graph2 = {
        'A': {'B': 3},
        'B': {'A': 3},
        'C': {'D': 2},
        'D': {'C': 2}
    }
    test_dijkstra(graph2, 'A', 'D', [])  # No path
    
    # 3. Graph with Negative Weights but No Negative Cycle
    graph3 = {
        'A': {'B': 2, 'C': 4},
        'B': {'A': 2, 'C': -1, 'D': 5},
        'C': {'A': 4, 'B': -1, 'D': 3},
        'D': {'B': 5, 'C': 3}
    }
    test_dijkstra(graph3, 'A', 'D', ['A', 'B', 'C', 'D'])

    # 4. Graph with Negative Cycle
    graph4 = {
        'A': {'B': 2, 'C': 4},
        'B': {'A': 2, 'C': -3, 'D': 5},
        'C': {'A': 4, 'B': -3, 'D': 3},
        'D': {'B': 5, 'C': 3}
    }
    test_dijkstra(graph4, 'A', 'D', [])  # Negative cycle detected

    # 5. Single Node Graph
    graph5 = {
        'A': {}
    }
    test_dijkstra(graph5, 'A', 'A', ['A'])

# # Test case 1: Simple graph
# graph1 = {
#     'A': {'B': 1, 'C': 4},
#     'B': {'A': 1, 'C': 2, 'D': 5},
#     'C': {'A': 4, 'B': 2, 'D': 1},
#     'D': {'B': 5, 'C': 1}
# }
# start1 = 'A'
# end1 = 'D'
# print("Test Case 1:")
# print(dijkstra(graph1, start1, end1))  # Expected output: ['A', 'C', 'D']

# # Test case 2: Disconnected graph
# graph2 = {
#     'A': {'B': 1, 'C': 4},
#     'B': {'A': 1},
#     'C': {'A': 4},
#     'D': {}
# }
# start2 = 'A'
# end2 = 'D'
# print("\nTest Case 2:")
# print(dijkstra(graph2, start2, end2))  # Expected output: Node D not in previous nodes. Unable to reconstruct full path. []

# # Test case 3: Graph with negative edge weights
# graph3 = {
#     'A': {'B': 1, 'C': -2},
#     'B': {'C': 3},
#     'C': {'D': 2},
#     'D': {}
# }
# start3 = 'A'
# end3 = 'D'
# print("\nTest Case 3:")
# print(dijkstra(graph3, start3, end3))  # Expected output: ['A', 'C', 'D']

# # Test case 4: Graph with a single node
# graph4 = {
#     'A': {}
# }
# start4 = 'A'
# end4 = 'A'
# print("\nTest Case 4:")
# print(dijkstra(graph4, start4, end4))  # Expected output: ['A']


# # Test case 5: Large graph with multiple paths
# graph5 = {
#     'A': {'B': 1, 'C': 4, 'E': 2},
#     'B': {'A': 1, 'C': 2, 'D': 5},
#     'C': {'A': 4, 'B': 2, 'D': 1, 'E': 3},
#     'D': {'B': 5, 'C': 1, 'E': 2},
#     'E': {'A': 2, 'C': 3, 'D': 2}
# }
# start5 = 'A'
# end5 = 'D'
# print("Test Case 5:")
# print(dijkstra(graph5, start5, end5))  # Expected output: ['A', 'B', 'C', 'D']

# # Test case 6: Graph with loops
# graph6 = {
#     'A': {'B': 1, 'C': 2},
#     'B': {'A': 1, 'C': 2},
#     'C': {'A': 2, 'B': 2, 'D': 3},
#     'D': {'C': 3}
# }
# start6 = 'A'
# end6 = 'D'
# print("\nTest Case 6:")
# print(dijkstra(graph6, start6, end6))  # Expected output: ['A', 'C', 'D']

# # Test case 7: Graph with negative cycles
# graph7 = {
#     'A': {'B': 1},
#     'B': {'C': -1},
#     'C': {'A': -1}
# }
# start7 = 'A'
# end7 = 'C'
# print("\nTest Case 7:")
# print(dijkstra(graph7, start7, end7))  # Expected output: Negative cycle detected. []

# # Test case 8: Empty graph
# graph8 = {}
# start8 = 'A'
# end8 = 'B'
# print("\nTest Case 8:")
# print(dijkstra(graph8, start8, end8))  # Expected output: Either A or B is not in the graph. []

# # Test case 9: Graph with unreachable nodes
# graph9 = {
#     'A': {'B': 1},
#     'B': {'C': 2},
#     'C': {},
#     'D': {'E': 3},
#     'E': {'F': 4},
#     'F': {}
# }
# start9 = 'A'
# end9 = 'F'
# print("\nTest Case 9:")
# print(dijkstra(graph9, start9, end9))  # Expected output: Node F not in previous nodes. Unable to reconstruct full path. []

# # Test case 10: Random graph with varying edge weights
# graph10 = {
#     'A': {'B': 3, 'C': 5},
#     'B': {'C': 1, 'D': 7},
#     'C': {'D': 2},
#     'D': {'E': 4},
#     'E': {}
# }
# start10 = 'A'
# end10 = 'E'
# print("\nTest Case 10:")
# print(dijkstra(graph10, start10, end10))  # Expected output: ['A', 'B', 'C', 'D', 'E']
