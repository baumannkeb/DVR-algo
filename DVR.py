import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import time

def find_node_table(num_nodes, edges, src):
    dist = [float("Inf")] * num_nodes
    dist[src-1] = 0

    print(edges)

    #https://www.programiz.com/dsa/bellman-ford-algorithm
    for _ in range(num_nodes):
        for s, d, w in edges:
            if dist[s-1] != float("Inf") and dist[s-1] + w < dist[d-1]:
                dist[d-1] = dist[s-1] + w

    return dist

#run algorithm without stopping with timer
def DVR_continous(graph, edges):
    start_time = time.perf_counter()
    nodes = graph.nodes
    num_nodes = len(nodes)
    print(num_nodes)

    all_dist = []
    for i in range(num_nodes):
        print(i)
        dist = find_node_table(num_nodes, edges, i+1)
        print(dist)
        all_dist.append(dist)

    print(all_dist)

    end_time = time.perf_counter()
    print("Reached stable state in: ", end_time-start_time, "seconds")
    return all_dist


# creates initial link state
def create_graph(data):
    #https://networkx.org/documentation/stable/tutorial.html
    graph = nx.Graph()
    for line in data:
        graph.add_edge(line[0], line[1])
        graph[line[0]][line[1]]['weight'] = line[2]
    pos = nx.spring_layout(graph)
    #https://stackoverflow.com/questions/28372127/add-edge-weights-to-plot-output-in-networkx/28372251
    nx.draw(graph,pos, with_labels = True)
    labels = nx.get_edge_attributes(graph,'weight')
    nx.draw_networkx_edge_labels(graph,pos,edge_labels=labels)

    plt.savefig("graph.png")
    return graph


#selects input file
def select_file():
    parsed_file = []
    while True:
        file = input("Enter the file you want to read from: ")
        try:
            fp = open(file, "r")
            while True:
                edge = []
                line = fp.readline()
                if not line:
                    break
                line = line.split()
                edge.append(int(line[0]))
                edge.append(int(line[1]))
                edge.append(float(line[2]))
                parsed_file.append(edge)
            return parsed_file
        except IOError:
            print("Something went wrong :(")


if __name__ == "__main__":
    file_input = select_file()
    graph = create_graph(file_input)
    DVR_continous(graph, file_input)

    #how to individually get elements of graph
    #for element in graph.edges.data():
        #print(element)