#https://pypi.org/project/networkx/
import networkx as nx
#pip install matplotlib
import matplotlib.pyplot as plt
import time
import os
#python -m pip install pysimplegui
import PySimpleGUI as sg

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
    for link in edges:
        print(link)
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

    print(edges)
    print(all_dist)

    plt.savefig("graph.png")
    plt.clf()


#selects input file
def select_file(file):
    while True:
        try:
            fp = open(file, "r")
            if os.path.exists("graph.png"):
                edges.clear()
                all_dist.clear()
                graph.clear()
                os.remove("graph.png")
            while True:
                edge = []
                line = fp.readline()
                if not line:
                    break
                line = line.split()
                edge.append(int(line[0]))
                edge.append(int(line[1]))
                edge.append(float(line[2]))
                edges.append(edge)
            return True
        except IOError:
            return False

layout_og = [
    [sg.Text("Enter the text file to read from and press ok"), sg.InputText('', size =(10,1), key='text_file')],
    [sg.Button("Ok")]
]

def show_image(success, text_file, window):
    if success:
        user_msg = text_file + " opened successfully"
        create_graph()
        layout_textfile = [
            [sg.Text("Enter the text file to read from and press ok"), sg.InputText('', size =(10,1), key='text_file')],
            [sg.Button("Ok")],
            [sg.Text(user_msg)],
            [sg.Image("graph.png")],
            [sg.Text("Press single step mode or continous mode to start or change a link cost"), sg.Button("Continous"), sg.Button("Single-Step")],
            [sg.Button("Exit")]
        ]
    else:
        layout_textfile = [
            [sg.Text("Enter the text file to read from and press ok"), sg.InputText('', size =(10,1), key='text_file')],
            [sg.Button("Ok")],
            [sg.Text("File did not open successfully, try again")],
            [sg.Button("Exit")]
        ]
    window1 = sg.Window("Distance Vector Routing simulation", location=location).Layout(layout_textfile)
    window.close()
    return window1

def start_GUI():
    window = sg.Window("Distance Vector Routing simulation", location=location).Layout(layout_og)

    while True:
        event, values = window.read()
        if event == "Ok":
            text_file = values['text_file']
            success = select_file(text_file)
            window = show_image(success, text_file, window)
        elif event == "Continous":
            DVR_continous()
        elif event == "Single-Step":
            DVR_singlestep()
        elif event == "Exit" or event == sg.WIN_CLOSED:
            break

    window.close()

if __name__ == "__main__":
    global location
    location = (600,600)
    global edges
    edges = []
    global all_dist
    all_dist = []
    global graph
    graph = nx.Graph()

    start_GUI()