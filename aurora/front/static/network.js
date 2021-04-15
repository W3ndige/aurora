var clusterIndex = 0;
var clusters = [];
var lastClusterZoomLevel = 0;
var clusterFactor = 0.9;

var container = document.getElementById('network');
var data = {
    nodes: {
        {
            nodes | safe
        }
    },
    edges: {
        {
            edges | safe
        }
    }
};

var options = {
    "configure": {
        "enabled": false
    },
    "edges": {
        "color": {
            "inherit": true
        },
        "smooth": {
            "enabled": false,
            "type": "continuous"
        }
    },
    "interaction": {
        "dragNodes": true,
        "hideEdgesOnDrag": false,
        "hideNodesOnDrag": false
    },
    "physics": {
        "barnesHut": {
            "avoidOverlap": 0,
            "centralGravity": 0.3,
            "damping": 0.09,
            "gravitationalConstant": -80000,
            "springConstant": 0.001,
            "springLength": 250
        },
        "enabled": true,
        "stabilization": {
            "enabled": true,
            "fit": true,
            "iterations": 1000,
            "onlyDynamicEdges": false,
            "updateInterval": 100
        }
    },
    "layout": {
        "improvedLayout": false
    }
}

var network = new vis.Network(container, data, options);

network.on("selectNode", function(params) {
    if (params.nodes.length == 1) {
        if (network.isCluster(params.nodes[0]) == true) {
            network.openCluster(params.nodes[0]);
        }
    }
});

network.once("beforeDrawing", function() {
    var clusterOptionsByData = {
        processProperties: function(clusterOptions, childNodes) {
            clusterOptions.label = "[" + childNodes.length + "]";
            clusterOptions.font = {
                size: childNodes.length + 50
            }
            return clusterOptions;
        },

        clusterNodeProperties: function(clusterOptions, childNodes) {
            clusterOptions.borderWidth = 3;
            clusterOptions.shape = "box";
            return clusterOptions
        },
    };
    network.clusterByHubsize(70, clusterOptionsByData);
});