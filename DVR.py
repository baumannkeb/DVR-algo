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
        new_row = []
        for j, item in enumerate(row):
            new_row.append(str(item))
        new_row.insert(0, str(i+1))
        data.append(new_row)

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
    #print("DVR_calc all_dist:", all_dist)

    dist = all_dist[node]
    #https://www.programiz.com/dsa/bellman-ford-algorithm
    for s, d, w in edges:
        #print(type(dist[s-1]), type(w), type(dist[d-1]))
        if float(dist[s-1]) != 16 and float(dist[s-1]) + w < float(dist[d-1]):
            dist[d-1] = float(dist[s-1]) + w
    all_dist[node] = dist

# single step mode for DVR algo
def DVR_singlestep(window, cycle_count):
    #print(edges)

    for i in range(len(all_dist)):
        #print("i: ", i)
        DVR_calc(i)
    cycle_count = cycle_count + 1
    table = create_table(graph.nodes, all_dist)
    
    if cycle_count < (len(all_dist)-1):
        layout_DVRsingle = [
            [sg.Text("Enter the text file to read from and press ok"), sg.InputText('', size =(10,1), key='text_file')],
            [sg.Button("Ok")],
            [sg.Image("graph.png"), sg.Button("Routing Tables")],
            [sg.Text("Press single step mode or continous mode to start or change a link cost"), sg.Button("Continous"), sg.Button("Single-Step")],
            [sg.Text("Cycle number: " + str(cycle_count))],
            [sg.Text("Distance Vector Table:")],
            [sg.Column(table)],
            [sg.Text("To change the a link cost: ")],
            [sg.Text("Enter the source and destination nodes in the first two blanks and the new link cost in the third, press change when done")],
            [sg.InputText('source node', size = (10,1), key='node1'), sg.InputText('dest node', size = (10,1), key='node2'), sg.InputText('new weight', size = (10,1), key='new_weight'), sg.Button("Change")],
            [sg.Button("Exit")]
        ]
    else:
        layout_DVRsingle = [
            [sg.Text("Enter the text file to read from and press ok"), sg.InputText('', size =(10,1), key='text_file')],
            [sg.Button("Ok")],
            [sg.Image("graph.png"), sg.Button("Routing Tables")],
            [sg.Text("Press single step mode or continous mode to start or change a link cost"), sg.Button("Continous"), sg.Button("Single-Step")],
            [sg.Text("Stable state reached! Cycle number: " + str(len(all_dist)-1))],
            [sg.Text("Distance Vector Table:")],
            [sg.Column(table)],
            [sg.Text("To change the a link cost: ")],
            [sg.Text("Enter the source and destination nodes in the first two blanks and the new link cost in the third, press change when done")],
            [sg.InputText('source node', size = (10,1), key='node1'), sg.InputText('dest node', size = (10,1), key='node2'), sg.InputText('new weight', size = (10,1), key='new_weight'), sg.Button("Change")],
            [sg.Button("Exit")]
        ]

    window1 = sg.Window("Distance Vector Routing simulation", location=location).Layout(layout_DVRsingle)
    window.close()
    return window1, cycle_count
    #print("current all_dist array: ", all_dist)
    #input("Press enter to continue....")
    #print("stable state!!")

# continous mode for DVR algo
def DVR_continous(window, line_down):
    #print("DVR_cont1 all_dist:", all_dist)
    start_time = time.perf_counter()
    for _ in range(len(all_dist)-1):
        for i in range(len(all_dist)):
            #print("i: ", i)
            DVR_calc(i)
    #print("DVR_cont2 all_dist:", all_dist)
    end_time = time.perf_counter()
    runtime = end_time - start_time

    table = create_table(graph.nodes, all_dist)

    if line_down:
          layout_DVRcont = [
            [sg.Text("Enter the text file to read from and press ok"), sg.InputText('', size =(10,1), key='text_file')],
            [sg.Button("Ok")],
            [sg.Image("graph.png"), sg.Button("Routing Tables")],
            [sg.Text("Distance Vector Table:")],
            [sg.Column(table)],
            [sg.Text("To change the a link cost: ")],
            [sg.Text("Enter the source and destination nodes in the first two blanks and the new link cost in the third, press change when done")],
            [sg.InputText('source node', size = (10,1), key='node1'), sg.InputText('dest node', size = (10,1), key='node2'), sg.InputText('new weight', size = (10,1), key='new_weight'), sg.Button("Change")],
            [sg.Text("Line is down! Change the cost back to what it was to fix the line")],
            [sg.Button("Exit")]
        ]
    else:
        layout_DVRcont = [
            [sg.Text("Enter the text file to read from and press ok"), sg.InputText('', size =(10,1), key='text_file')],
            [sg.Button("Ok")],
            [sg.Image("graph.png"), sg.Button("Routing Tables")],
            [sg.Text("Press single step mode or continous mode to start or change a link cost"), sg.Button("Continous"), sg.Button("Single-Step")],
            [sg.Text("Stable state reached in " + str(runtime) + " secs")],
            [sg.Text("Distance Vector Table:")],
            [sg.Column(table)],
            [sg.Text("To change the a link cost: ")],
            [sg.Text("Enter the source and destination nodes in the first two blanks and the new link cost in the third, press change when done")],
            [sg.InputText('source node', size = (10,1), key='node1'), sg.InputText('dest node', size = (10,1), key='node2'), sg.InputText('new weight', size = (10,1), key='new_weight'), sg.Button("Change")],
            [sg.Button("Exit")]
        ]

    window1 = sg.Window("Distance Vector Routing simulation", location=location).Layout(layout_DVRcont)
    window.close()
    return window1

# allows user to change link costs and updates DVs with single step mode
def adjust_linkcost(N1, N2, new_cost, window, old_cost):
    print(edges)
    for edge in edges:
        if edge[0] == int(N1) and edge[1] == int(N2):
            if new_cost == float(16):
                old_cost = edge[2]
                edge[2] = new_cost
                print(edges)
                create_graph()
                window = DVR_continous(window, True)
                return window, old_cost
            elif new_cost == old_cost and edge[2] == float(16):
                old_cost = -1
                edge[2] = new_cost
                print(edges)
                create_graph()
                window = DVR_continous(window, False)
                return window, old_cost
            else:
                old_cost = -1
                edge[2] = new_cost
                print(edges)
                create_graph()
                window = DVR_continous(window, False)
                return window, old_cost
    return window, -1

def display_routing_tables():
    data = []
    cols = 2
    rows = len(graph.nodes) * len(graph.nodes)

    # node_info is array of arrays of nodes
    for i, node_info in enumerate(routing_table):
        source_node = "Next node from source node: " + str((i+1))
        data.append(["Dest nodes", source_node])
        # next_node is each individual array inside node_info
        for j, next_node in enumerate(node_info):
            print(i,j)
            print(node_info, next_node)
            if i != j:
                if next_node[0] == 0:
                    data.append([str(j+1), "None"])
                else:
                    data.append([str(j+1), str(next_node[1])])

    table = []
    print(table)
    #https://github.com/PySimpleGUI/PySimpleGUI/issues/3528#issuecomment-715665600
    for y in range(0, rows):
        line = []
        for x in range(0, cols):
            bg = 'blue' if (x == 0 ) else 'orange'
            line.append(
                sg.Text(data[y][x], size = (30,1), justification = 'c',
                text_color = 'white', background_color = bg)
            )
        table.append(line)
    print(table)
    location = (1200, 100)
    layout = [
        [sg.Column(table, background_color='black', key='Table')]
    ]

    window1 = sg.Window('Routing tables',location=location).Layout(layout)

    event, values = window1.read()

    return

# finds the node to go to in order to get to the destination for all nodes
def find_routing_tables():
    print(graph.nodes)
    print(graph.edges)
    print
    for src in graph.nodes:
        path = []
        for dest in graph.nodes:
            if src != dest:
                try:
                    curr_path = nx.shortest_path(graph, source=src, target=dest, weight='weight')
                    path.append(curr_path)
                except:
                    path.insert(dest-1,[0])
            else:
                path.append([0])
        routing_table.append(path)


# creates initial graph and initializes a bunch of stuff
def create_graph():
    if os.path.exists("graph.png"):
        routing_table.clear()
        all_dist.clear()
        graph.clear()
        os.remove("graph.png")
    #print("create_graph all_dist:", all_dist)
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
            [sg.Image("graph.png"), sg.Button("Routing Tables")],
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
    old_cost = -1
    cycle_count = 0

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
        elif event == "Routing Tables":
            find_routing_tables()
            display_routing_tables()
        elif event == "Continous":
            window = DVR_continous(window, False)
        elif event == "Single-Step":
            window, cycle_count = DVR_singlestep(window, cycle_count)
        elif event == "Change":
            node1 = values['node1']
            node2 = values['node2']
            new_weight = values['new_weight']
            if node1 and node2 and new_weight and float(new_weight) >= float(0) and float(new_weight) <= float(16):
                window, old_cost = adjust_linkcost(int(node1), int(node2), float(new_weight), window, old_cost)
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
    global routing_table
    routing_table = []
    global graph
    graph = nx.DiGraph()

    start_GUI()