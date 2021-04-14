import networkx as nx
import matplotlib.pyplot as plt
import time
from multiprocessing import Pool

def DVR_singlestep(node):
    print("node number: ",node)

    """
    for s, d, w in edges:
        if dist[s-1] != float("Inf") and dist[s-1] + w < dist[d-1]:
            dist[d-1] = dist[s-1] + w
    """

def pool_handler():
    p = Pool(4)
    for i in range(len(all_dist)):
        print("i: ", i)
        result = p.map(DVR_singlestep, all_dist)

"""
def find_node_table(num_nodes, src):
    dist = [float("Inf")] * num_nodes
    dist[src-1] = 0

    print(edges)

    #https://www.programiz.com/dsa/bellman-ford-algorithm
    for _ in range(num_nodes-1):
        for s, d, w in edges:
            if dist[s-1] != float("Inf") and dist[s-1] + w < dist[d-1]:
                dist[d-1] = dist[s-1] + w

    return dist

#run algorithm without stopping with timer
def DVR_continous():
    start_time = time.perf_counter()

    all_dist = []
    for i in range(len(list_nodes)):
        print(i)
        dist = find_node_table(len(list_nodes), i+1)
        print(dist)
        all_dist.append(dist)

    print(all_dist)

    end_time = time.perf_counter()
    print("Reached stable state in: ", end_time-start_time, "seconds")
    return all_dist
"""

# creates initial link state
def create_graph():
    global all_dist
    #https://networkx.org/documentation/stable/tutorial.html
    graph = nx.Graph()
    for link in edges:
        graph.add_edge(link[0], link[1])
        graph[link[0]][link[1]]['weight'] = link[2]
    pos = nx.spring_layout(graph)
    #https://stackoverflow.com/questions/28372127/add-edge-weights-to-plot-output-in-networkx/28372251
    nx.draw(graph, pos, with_labels = True)
    labels = nx.get_edge_attributes(graph,'weight')
    nx.draw_networkx_edge_labels(graph,pos,edge_labels=labels)

    for i in range(len(graph.nodes)):
        initial_table = [float("Inf")] * len(graph.nodes)
        initial_table[i] = 0
        initial_table.insert(0, i+1)
        all_dist.append(initial_table)

    print(all_dist)

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
    global edges
    edges = []
    global all_dist
    all_dist = []

    edges = select_file()
    graph = create_graph()
    pool_handler()
    #DVR_continous()

    #how to individually get elements of graph
    #for element in graph.edges.data():
        #print(element)