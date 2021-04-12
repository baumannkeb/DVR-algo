import networkx as nx
import matplotlib.pyplot as plt

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

    #how to individually get elements of graph
    for element in graph.edges.data():
        print(element)
    print(graph.edges.data())
    print(graph.edges)
    print(graph.nodes)



def select_file():
    parsed_file = []
    while True:
        file = input("Enter the file you want to read from: ")
        try:
            fp = open(file, "r")
            while True:
                line = fp.readline()
                if not line:
                    break
                line = line.split()
                parsed_file.append(line)
            return parsed_file
        except IOError:
            print("Something went wrong :(")


if __name__ == "__main__":
    file_input = select_file()
    create_graph(file_input)