#https://pypi.org/project/networkx/
import networkx as nx
#pip install matplotlib
import matplotlib.pyplot as plt
#python -m pip install pysimplegui
import PySimpleGUI as sg
import time
import os

#create table
def create_table(nodes, weights):
    headers = []
    for node in nodes:
        headers.append(str(node))

    size = len(headers) + 1
    
    data = []
    headers.insert(0, "Nodes")
    data.append(headers)
    for i, row in enumerate(weights):
        for j, item in enumerate(row):
            row[j] = str(item)
        row.insert(0, str(i+1))
        data.append(row)

    table = []
    #https://github.com/PySimpleGUI/PySimpleGUI/issues/3528#issuecomment-715665600
    for y in range(0, size):
        line = []
        for x in range(0, size):
            bg = 'blue' if (x == 0 or y == 0) else 'orange'
            line.append(
                sg.Text(data[y][x], size = (10,1), justification = 'c',
                text_color = 'white', background_color = bg)
            )
        table.append(line)

    return table  

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
# TODO: implement single step mode in GUI with the Single-step button to start each step
# make sure to save number of cycles it took to reach stable state
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
def DVR_continous(window):
    start_time = time.perf_counter()
    for _ in range(len(all_dist)-1):
        for i in range(len(all_dist)):
            #print("i: ", i)
            DVR_calc(i)

    end_time = time.perf_counter()
    runtime = end_time - start_time

    table = create_table(graph.nodes, all_dist)

    layout_DVRcont = [
        [sg.Text("Enter the text file to read from and press ok"), sg.InputText('', size =(10,1), key='text_file')],
        [sg.Button("Ok")],
        [sg.Image("graph.png")],
        [sg.Text("Press single step mode or continous mode to start or change a link cost"), sg.Button("Continous"), sg.Button("Single-Step")],
        [sg.Text("Stable state reached in " + str(runtime) + " secs")],
        [sg.Text("Distance Vector Table:")],
        [sg.Column(table)],
        [sg.Text("Enter the link cost you want to alter, enter the two nodes at the ends of the link in the first two blanks and the new link cost in the third, press change when done")],
        [sg.InputText('node 1', size = (10,1), key='node1'), sg.InputText('node 2', size = (10,1), key='node2'), sg.InputText('new weight', size = (10,1), key='new_weight'), sg.Button("Change")],
        [sg.Button("Exit")]
        ]

    window1 = sg.Window("Distance Vector Routing simulation", location=location).Layout(layout_DVRcont)
    window.close()
    return window1

# allows user to change link costs and updates DVs with single step mode
# TODO: implement changing link cost in gui, check for if link is valid, new cost is 16 and cost is 0-16
def adjust_linkcost(N1, N2, new_weight):
    print(N1, N2, new_weight)
    """
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
    """

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
    nx.draw_networkx_edge_labels(graph,pos,edge_labels=labels, arrowsize = 20, arrowstyle = 'fancy')

    for i in range(len(graph.nodes)):
        initial_table = [16] * len(graph.nodes)
        initial_table[i] = 0
        all_dist.append(initial_table)

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

# TODO: display routing table for each node, I kinda jumped the gun with the actual graph but it's a cool feature
def start_GUI():
    layout_og = [
        [sg.Text("Enter the text file to read from and press ok"), sg.InputText('', size =(10,1), key='text_file')],
        [sg.Button("Ok")],
        [sg.Button("Exit")]
    ]
    window = sg.Window("Distance Vector Routing simulation", location=location).Layout(layout_og)

    while True:
        event, values = window.read()
        if event == "Ok":
            text_file = values['text_file']
            success = select_file(text_file)
            window = show_image(success, text_file, window)
        elif event == "Continous":
            window = DVR_continous(window)
        elif event == "Single-Step":
            DVR_singlestep()
        elif event == "Change":
            node1 = values['node1']
            node2 = values['node2']
            new_weight = values['new_weight']
            if node1 and node2 and new_weight:
                adjust_linkcost(node1, node2, new_weight)
        elif event == "Exit" or event == sg.WIN_CLOSED:
            break
    
    window.close()

if __name__ == "__main__":
    global location
    location = (500,100)
    global edges
    edges = []
    global all_dist
    all_dist = []
    global graph
    graph = nx.DiGraph()

    start_GUI()