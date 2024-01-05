from flask import Flask, render_template, request, jsonify
import heapq
from dijkstra import dijkstra

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shortest_path', methods=['POST'])
def compute_shortest_path():
    data = request.get_json()
    start_node = data['start']
    end_node = data['end']

    print("Start node: ", start_node)
    print("End node: ", end_node)

    # Extract and transform graph data
    graph = {}
    for start, ends in data['graph']['edges'].items():
        if start not in graph:
            graph[start] = {}
        for end in ends:
            edge_key = tupleString(start, end)
            graph[start][end] = int(data['graph']['weights'][edge_key])
            if end not in graph:  # Ensure every node appears as a key
                graph[end] = {}

    print("Graph: ", graph)
    path = dijkstra(graph, start_node, end_node)
    return jsonify({"path": path})

def tupleString(a, b):
    return a + "," + b if a < b else b + "," + a

if __name__ == '__main__':
    app.run(debug=True)
