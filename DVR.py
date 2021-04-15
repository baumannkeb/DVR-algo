import networkx as nx
import matplotlib.pyplot as plt
import time

# DVR algorithm 
def DVR_calc(node):
    #print("node number: ",node)

    dist = all_dist[node]
    #https://www.programiz.com/dsa/bellman-ford-algorithm
    for s, d, w in edges:
        if dist[s-1] != 16 and dist[s-1] + w < dist[d-1]:
            dist[d-1] = dist[s-1] + w
    all_dist[node] = dist

# single step mode for DVR algo
def DVR_singlestep():
    print(edges)
    for _ in range(len(all_dist)-1):
        for i in range(len(all_dist)):
            #print("i: ", i)
            DVR_calc(i)
        print("current all_dist array: ", all_dist)
        input("Press enter to continue....")
    print("stable state!!")

# continous mode for DVR algo
def DVR_continous():
    start_time = time.perf_counter()
    for _ in range(len(all_dist)-1):
        for i in range(len(all_dist)):
            #print("i: ", i)
            DVR_calc(i)

    end_time = time.perf_counter()
    print("stable state!!")
    print("Reached stable state in: ", end_time-start_time, "seconds")
    print("final all_dist array: ",all_dist)

# allows user to change link costs and updates DVs with single step mode
def adjust_linkcost():
    print("Links:")
    for i in range(len(edges)):
        print("#", i, ": ",edges[i])
    edge_to_adjust = int(input("What link cost would you like to change?"))
    new_cost = float(input("What would cost would you like to change it to?"))
    if new_cost == 16:
        print(edge_to_adjust+1," line down!")
        old_cost = edges[edge_to_adjust][2]
        edges[edge_to_adjust][2] = new_cost
        time.sleep(5)
        new_cost = old_cost
    edges[edge_to_adjust][2] = new_cost
    DVR_singlestep()

# creates initial graph and initializes a bunch of stuff
def create_graph():
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
        initial_table = [16] * len(graph.nodes)
        initial_table[i] = 0
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
    DVR_continous()
    #DVR_singlestep()
    adjust_linkcost()
    print(edges)