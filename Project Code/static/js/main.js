const canvas = document.getElementById('graphCanvas');
const ctx = canvas.getContext('2d');

let graphData = {
    nodes: {},
    edges: {},
    weights: {}
};

let selectedNodes = [];

let tooltip = document.createElement("div");
tooltip.classList.add("tooltip");
document.body.appendChild(tooltip);

canvas.addEventListener('click', function(event) {
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    const clickedNodeId = getNodeAtPosition(x, y);
    
    // Check if we clicked on a node
    if (clickedNodeId !== null) {
        if (selectedNodes.length === 0 || (selectedNodes.length === 1 && selectedNodes[0] !== clickedNodeId)) {
            selectedNodes.push(clickedNodeId);
        }

        if (selectedNodes.length === 2) {
            const edgeKey = tupleString(selectedNodes[0], selectedNodes[1]);
            if (!graphData.weights[edgeKey]) {
                const weight = prompt("Enter weight for this edge:", "1");
                if (weight) {
                    addEdge(selectedNodes[0], selectedNodes[1], weight);
                }
            }
            selectedNodes = [];
        }
    } else {
        // If a node is selected, clicking on empty space resets the temporary edge
        if (selectedNodes.length === 1) {
            selectedNodes = [];
        } else {
            addNode(x, y);
        }
    }
    drawGraph();
});

function getNodeAtPosition(x, y) {
    for (let nodeId in graphData.nodes) {
        const node = graphData.nodes[nodeId];
        const distance = Math.sqrt((node.x - x)**2 + (node.y - y)**2);
        if (distance < 20) {
            return nodeId;
        }
    }
    return null;
}

function addNode(x, y) {
    const nodeId = String.fromCharCode(65 + Object.keys(graphData.nodes).length);
    graphData.nodes[nodeId] = { x: x, y: y };
    updateDropdowns();
}

function addEdge(start, end, weight) {
    if (start === end) return; 
    const edgeKey = tupleString(start, end);

    if (graphData.weights[edgeKey]) return;

    graphData.edges[start] = graphData.edges[start] || [];
    graphData.edges[start].push(end);
    graphData.weights[edgeKey] = weight;
    updateDropdowns();
}

function tupleString(a, b) {
    return a < b ? `${a},${b}` : `${b},${a}`;
}

function updateDropdowns() {
    const startDropdown = document.getElementById("startNode");
    const endDropdown = document.getElementById("endNode");

    startDropdown.innerHTML = "";
    endDropdown.innerHTML = "";

    for (let nodeId in graphData.nodes) {
        const option = document.createElement("option");
        option.value = nodeId;
        option.textContent = nodeId;

        const option2 = option.cloneNode(true);
        startDropdown.appendChild(option);
        endDropdown.appendChild(option2);
    }
}

function drawGraph(highlightPath = [], currentStep = 0) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.font = "16px Arial";  // Set font size to 16px Arial as per the original requirement

    // Draw all edges in black first
    for (let start in graphData.edges) {
        for (let end of graphData.edges[start]) {
            const startNode = graphData.nodes[start];
            const endNode = graphData.nodes[end];
            ctx.beginPath();
            ctx.moveTo(startNode.x, startNode.y);
            ctx.lineTo(endNode.x, endNode.y);
            ctx.strokeStyle = 'black';
            ctx.stroke();
            const edgeKey = tupleString(start, end);
            const midX = (startNode.x + endNode.x) / 2;
            const midY = (startNode.y + endNode.y) / 2;
            ctx.fillText(graphData.weights[edgeKey], midX, midY);
        }
    }

    // Draw all nodes in white with black borders
    for (let nodeId in graphData.nodes) {
        const node = graphData.nodes[nodeId];
        ctx.beginPath();
        ctx.arc(node.x, node.y, 20, 0, 2 * Math.PI);
        ctx.fillStyle = selectedNodes.includes(nodeId) ? 'blue' : 'white'; // Highlight selected nodes in blue
        ctx.fill();
        ctx.strokeStyle = 'black';
        ctx.stroke();
        ctx.fillStyle = 'black';
        ctx.fillText(nodeId, node.x - ctx.measureText(nodeId).width / 2, node.y + 5);
    }
    // Immediately draw the first node if present
    if (highlightPath.length > 0) {
        const firstNode = graphData.nodes[highlightPath[0]];
        ctx.beginPath();
        ctx.arc(firstNode.x, firstNode.y, 20, 0, 2 * Math.PI);
        ctx.fillStyle = 'red';
        ctx.fill();
        ctx.strokeStyle = 'black';
        ctx.stroke();
        ctx.fillStyle = 'black';
        ctx.fillText(highlightPath[0], firstNode.x - ctx.measureText(highlightPath[0]).width / 2, firstNode.y + 5);
    }

    // Highlight the path nodes and edges with a delay
    if (currentStep > 1) {
        for (let i = 1; i < currentStep; i++) {
            let start = highlightPath[i - 1];
            let end = highlightPath[i];
            let startNode = graphData.nodes[start];
            let endNode = graphData.nodes[end];

            // Draw highlighted edge
            ctx.beginPath();
            ctx.moveTo(startNode.x, startNode.y);
            ctx.lineTo(endNode.x, endNode.y);
            ctx.strokeStyle = 'red';
            ctx.stroke();

            // Draw highlighted end node
            ctx.beginPath();
            ctx.arc(endNode.x, endNode.y, 20, 0, 2 * Math.PI);
            ctx.fillStyle = 'red';
            ctx.fill();
            ctx.strokeStyle = 'black';
            ctx.stroke();
            ctx.fillStyle = 'black';
            ctx.fillText(end, endNode.x - ctx.measureText(end).width / 2, endNode.y + 5);
        }
    }
}

document.getElementById("computePathBtn").addEventListener("click", async function() {
    const startNode = document.getElementById("startNode").value;
    const endNode = document.getElementById("endNode").value;
    if (startNode && endNode) {
        const data = {
            start: startNode,
            end: endNode,
            graph: graphData
        };

        console.log("Sending graph data to server:", data);

        const response = await fetch('/shortest_path', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        console.log("Response from server:", result);

        const shortestPath = result.path;
        if (shortestPath.length === 0) {
            alert("No path found!");
        } else {
            // Calculate the sum of distances
            let pathSum = 0;
            for (let i = 0; i < shortestPath.length - 1; i++) {
                const edgeKey = tupleString(shortestPath[i], shortestPath[i + 1]);
                pathSum += parseFloat(graphData.weights[edgeKey]);
            }
            // Display the sum of distances
            document.getElementById("pathSum").textContent = `Shortest Path Sum of Distances: ${pathSum}`;

            drawGraph(shortestPath, 1);  // Draw the first node immediately
            for (let i = 1; i <= shortestPath.length; i++) {
                setTimeout(() => {
                    drawGraph(shortestPath, i + 1);
                }, 1000 * i);
            }
        }
    }
});

document.getElementById("resetGraph").addEventListener("click", function(){

    location.reload()

});


updateDropdowns();


canvas.addEventListener('mousemove', function(event) {
    // Extract the cursor's coordinates
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    // If one node is selected, change cursor to indicate edge creation and draw a temporary edge
    if (selectedNodes.length === 1) {
        drawGraph();  // Redraw the canvas to clear previous temporary edges

        const startNode = graphData.nodes[selectedNodes[0]];
        ctx.beginPath();
        ctx.moveTo(startNode.x, startNode.y);
        ctx.lineTo(x, y);
        ctx.strokeStyle = '#aaa';
        ctx.setLineDash([5, 3]);
        ctx.stroke();
        ctx.setLineDash([]); // Reset to solid line

        // Change cursor
        if (getNodeAtPosition(x, y)) {
            canvas.style.cursor = 'pointer'; // Indicate edge creation with existing node
        } else {
            canvas.style.cursor = 'crosshair'; // Indicate edge creation with new node
        }
    } else {
        canvas.style.cursor = 'default';
    }

    // Show tooltips for edges (showing weight)
    const edgeKey = Object.keys(graphData.weights).find(eKey => {
        const [startId, endId] = eKey.split(',');
        const start = graphData.nodes[startId];
        const end = graphData.nodes[endId];
        const midX = (start.x + end.x) / 2;
        const midY = (start.y + end.y) / 2;
        return Math.abs(midX - x) < 10 && Math.abs(midY - y) < 10;
    });

    if (edgeKey) {
        tooltip.textContent = graphData.weights[edgeKey];
        tooltip.style.left = event.pageX + 10 + 'px';
        tooltip.style.top = event.pageY + 10 + 'px';
        tooltip.style.opacity = 1;
    } else {
        tooltip.style.opacity = 0;
    }
});



