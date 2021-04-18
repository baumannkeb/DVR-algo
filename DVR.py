# pip install networkx
import networkx as nx
# pip install matplotlib
import matplotlib.pyplot as plt
# pip install pysimplegui
import PySimpleGUI as sg
import time
import os
# Inputs: nodes of the network, the DVR information calculated
# Outputs: formatted table for the DVR information
# Purpose: Formats distance vector routing information into a displayable table for the GUI
def create_table(nodes, distances):
    # list to hold headers of the DVR table whichh will be the first row of the table
    headers = []

    # appending each node to the header
    for i in range(len(nodes)):
        headers.append(str(i+1))
    # saving the size of the table which will have equal rows and columns
    size = len(headers) + 1
    # inserting a node label to the beginning of the headers list
    headers.insert(0, "Nodes")

# list to hold the shortest calculated distances from the source node to the destination node
    data = []
    # appending the headers to the first spot in the data array
    data.append(headers)

    # forming the rest of the table
    for i, row in enumerate(distances):
        # list for storing the distances in the proper order
        new_row = []
        # for each distance in the row of the weights list
        for item in row:
            # append all items from the row
            new_row.append(str(item))
        # insert the node number in the first spot of the new row list
        new_row.insert(0, str(i+1))
        # append the new row into the data list
        data.append(new_row)

    # list to use to format the data list into the table to display on the GUI
    table = []
    # Used link below for information on how to format a list into a table
    # https://github.com/PySimpleGUI/PySimpleGUI/issues/3528#issuecomment-715665600
    for y in range(0, size):
        line = []
        for x in range(0, size):
            # the first row and column will be blue, the rest will be orange
            bg = 'blue' if (x == 0 or y == 0) else 'orange'
            # formating the data and appending it to a new list
            line.append(
                sg.Text(data[y][x], size = (10,1), justification = 'c',
                text_color = 'white', background_color = bg)
            )
        # appending the formatted line list to the table
        table.append(line)
    # returning the table list
    return table  

# Inputs: node to calculate the DVR table for
# Outputs: None
# Purpose: Calculates the Distance Vector Routing information for the passed in node
def DVR_calc(node):
    # saving the list at the node index of the all_dist list
    dist = all_dist[node]

    # Used link below for bellman-ford algorithm
    # https://www.programiz.com/dsa/bellman-ford-algorithm
    # for each source node, destination node and weight in the edges list
    for s, d, w in edges:
        # if the distance from the node is not infinity (shown as 16) and the distance plus the weight is less than the already saved distance
        if float(dist[s-1]) != 16 and float(dist[s-1]) + w < float(dist[d-1]):
            # changed the saved distance to the new distance
            dist[d-1] = float(dist[s-1]) + w
    # insert the dist list into the all_dist list
    all_dist[node] = dist

# Inputs: window of GUI, cycle count of number of cycles run
# Outputs: updated window for GUI
# Purpose: Finds the Distance Vector Routing information in single step mode for each node
def DVR_singlestep(window, cycle_count):
    # if single step mode has not been run yet
    if cycle_count == 0:
        # clear the all_dist list
        all_dist.clear()
        # recreate graph 
        create_graph()

    # len(all_dist) will always be the number of nodes so DVR_calc will run for each node
    for i in range(len(all_dist)):
        DVR_calc(i)

    # increment cycle_count to keep track of how many cycles have run
    cycle_count = cycle_count + 1
    # create the formatted table of DVR values
    table = create_table(graph.nodes, all_dist)
    
    # if the cycle count is one less than the number of nodes, show the nodes have reached a stable state
    if cycle_count < (len(all_dist)-1):
        # GUI layout for DVR single-step mode with stable state reached
        layout_DVRsingle = [
            [sg.Text("Enter the text file to read from and press ok"), sg.InputText('', size =(10,1), key='text_file')],
            [sg.Button("Ok")],
            [sg.Image("graph.png"), sg.Button("Routing Tables")],
            [sg.Text("Press single step mode, continous mode, reset or change a link cost"), sg.Button("Continous"), sg.Button("Single-Step"), sg.Button("Reset")],
            [sg.Text("Cycle number: " + str(cycle_count))],
            [sg.Text("Distance Vector Table:")],
            [sg.Column(table)],
            [sg.Text("To change the a link cost: ")],
            [sg.Text("Enter the source and destination nodes in the first two blanks and the new link cost in the third, press change when done")],
            [sg.InputText('source node', size = (10,1), key='node1'), sg.InputText('dest node', size = (10,1), key='node2'), sg.InputText('new weight', size = (10,1), key='new_weight'), sg.Button("Change")],
            [sg.Button("Exit")]
        ]
    else:
        # GUI layout for DVR single-step mode without stable state reached
        layout_DVRsingle = [
            [sg.Text("Enter the text file to read from and press ok"), sg.InputText('', size =(10,1), key='text_file')],
            [sg.Button("Ok")],
            [sg.Image("graph.png"), sg.Button("Routing Tables")],
            [sg.Text("Press single step mode, continous mode, reset or change a link cost"), sg.Button("Continous"), sg.Button("Single-Step"), sg.Button("Reset")],
            [sg.Text("Stable state reached! Cycle number: " + str(len(all_dist)-1))],
            [sg.Text("Distance Vector Table:")],
            [sg.Column(table)],
            [sg.Text("To change the a link cost: ")],
            [sg.Text("Enter the source and destination nodes in the first two blanks and the new link cost in the third, press change when done")],
            [sg.InputText('source node', size = (10,1), key='node1'), sg.InputText('dest node', size = (10,1), key='node2'), sg.InputText('new weight', size = (10,1), key='new_weight'), sg.Button("Change")],
            [sg.Button("Exit")]
        ]

    # create a window for the new layout
    window1 = sg.Window("Distance Vector Routing simulation", location=location).Layout(layout_DVRsingle)
    # close the old window
    window.close()
    # return the new window and the cycle count to keep track of the number of cycles
    return window1, cycle_count

# Inputs: window of GUI, boolean value if the line is down or not, the old cost of the link 
# Outputs: updated window for GUI
# Purpose: Finds the Distance Vector Routing information in continous mode for each node, also has layout for if a line is down
def DVR_continous(window, line_down, old_cost):
    # record the start time of the DVR_continous function
    start_time = time.perf_counter()
    # The maximum number of times DVR calc will ever need to be run is one less than the number of nodes
    # because the number of edges that could be between the two farthest nodes is one less than the number of nodes
    # for example the max number of edges between two nodes in a graph of 4 nodes would be 3
    for _ in range(len(all_dist)-1):
        for i in range(len(all_dist)):
            DVR_calc(i)
    
    # record the end time after the DVR table has been calculated for all nodes in continous mode
    end_time = time.perf_counter()
    # subtract the endtime and starttime to get the total run time
    runtime = end_time - start_time

    # create the formatted table of DVR values
    table = create_table(graph.nodes, all_dist)

    # if the line is down, display that on the GUI and take away the options of running continous or single step mode
    if line_down:
        #layout for DVR continous and when the line is down
        layout_DVRcont = [
            [sg.Text("Enter the text file to read from and press ok"), sg.InputText('', size =(10,1), key='text_file')],
            [sg.Button("Ok")],
            [sg.Image("graph.png"), sg.Button("Routing Tables")],
            [sg.Text("Distance Vector Table:")],
            [sg.Column(table)],
            [sg.Text("To change the a link cost: ")],
            [sg.Text("Enter the source and destination nodes in the first two blanks and the new link cost in the third, press change when done")],
            [sg.InputText('source node', size = (10,1), key='node1'), sg.InputText('dest node', size = (10,1), key='node2'), sg.InputText('new weight', size = (10,1), key='new_weight'), sg.Button("Change")],
            [sg.Text("Line is down! Change the cost back to what it was, " + str(old_cost) + ", to fix the line")],
            [sg.Button("Exit")]
        ]
    else:
        # layout for DVR continous normal
        layout_DVRcont = [
            [sg.Text("Enter the text file to read from and press ok"), sg.InputText('', size =(10,1), key='text_file')],
            [sg.Button("Ok")],
            [sg.Image("graph.png"), sg.Button("Routing Tables")],
            [sg.Text("Press single step mode, continous mode, reset or change a link cost"), sg.Button("Continous"), sg.Button("Single-Step"), sg.Button("Reset")],
            [sg.Text("Stable state reached in " + str(runtime) + " secs")],
            [sg.Text("Distance Vector Table:")],
            [sg.Column(table)],
            [sg.Text("To change the a link cost: ")],
            [sg.Text("Enter the source and destination nodes in the first two blanks and the new link cost in the third, press change when done")],
            [sg.InputText('source node', size = (10,1), key='node1'), sg.InputText('dest node', size = (10,1), key='node2'), sg.InputText('new weight', size = (10,1), key='new_weight'), sg.Button("Change")],
            [sg.Button("Exit")]
        ]

    # create window for new layout
    window1 = sg.Window("Distance Vector Routing simulation", location=location).Layout(layout_DVRcont)
    # close the old window
    window.close()
    # return the new window
    return window1

# Inputs: source node of link to change, dest node of link to change, window of the GUI, old cost of the line if applicable, previously changed source node, and previously changed dest node
# Outputs: updated window of GUI, old cost of the line if applicable, previously changed source node, and previously changed dest node
# Purpose: Allows the user to change the link cost between any two nodes, all simulates a line being "down"
def adjust_linkcost(N1, N2, new_cost, window, old_cost, changed_N1, changed_N2):
    # going through all edges to see if the two input nodes have a valid link
    for edge in edges:
        # if the link is found
        if edge[0] == int(N1) and edge[1] == int(N2):
            # if the new cost is 16, simulate a line being down
            if new_cost == float(16):
                # save the old cost of the link to check if the line is back "up"
                old_cost = edge[2]
                # save the old source node of the link to check if the user is putting the line back up for the line down
                changed_N1 = edge[0]
                # save the old dest node of the link to check if the user is putting the line back up for the line down
                changed_N2 = edge[1]
                # save the new cost input by the user in the edges list
                edge[2] = new_cost
                # create a new graph to show the effect of the line being down
                create_graph()
                # running DVR continous to update the DVR table
                window = DVR_continous(window, True, old_cost)
            # if the user is changing back the down line to the previous cost, the line is being fixed
            elif new_cost == old_cost and edge[2] == float(16) and changed_N1 == N1 and changed_N2 == N2:
                # setting the old cost back to -1
                old_cost = -1
                # setting the changed source node back to -1
                changed_N1 = -1
                # setting the changed dest node back to -1
                changed_N2 = -1
                # save the new cost input by the user in the edges list
                edge[2] = new_cost
                # create a new graph to show the line being fixed
                create_graph()
                # running DVR continous to update the DVR table
                window = DVR_continous(window, False, 0)
            # if the old cost is -1 meaning a line is not currently down, any link can be changed
            elif old_cost == -1:
                # save the new cost input by the user in the edges list
                edge[2] = new_cost
                # create a new graph to show effect of the changed line
                create_graph()
                # running DVR continous to update the DVR table
                window = DVR_continous(window, False, 0)

    # returning the window for the GUI, the old cost, changed source node and changed dest node to keep track of them
    return window, old_cost, changed_N1, changed_N2

# Inputs: none
# Outputs: none
# Purpose: display the calculate routing tables for each node
def display_routing_tables():
    # list to hold the information to be formmatted into the table 
    data = []
    # number of columns for the routing table display
    cols = 2
    # number of rows for the routing table display will be the number of nodes times the number of nodes
    # because even though we won't show the same node going to the same node, we will want an extra row for a header to divide up the nodes
    rows = len(graph.nodes) * len(graph.nodes)

    # going through each list inside the routing table list
    for i, node_info in enumerate(routing_table):
        # creating a header to go in between each routing table for each node
        source_node = "Next node from source node: " + str((i+1))
        # header to denote the destination nodes
        data.append(["Dest nodes", source_node])
        # next_node is each individual array inside node_info
        for j, next_node in enumerate(node_info):
            # if the node numbers do not match ( we don't care about the path between the same nodes )
            if i != j:
                # if it is zero, insert the value of none to show there is no path in between these nodes
                if next_node[0] == 0:
                    data.append([str(j+1), "None"])
                else:
                    # if there is a path, append the next node for the source node
                    data.append([str(j+1), str(next_node[1])])
    
    # list to store the formatted information to display on the GUI
    table = []

    for y in range(0, rows):
        line = []
        for x in range(0, cols):
            # if it is the first column, make the background blue
            bg = 'blue' if (x == 0 ) else 'orange'
            # append the formatted data to the line list
            line.append(
                sg.Text(data[y][x], size = (30,1), justification = 'c',
                text_color = 'white', background_color = bg)
            )
        # append the total line list to the table list
        table.append(line)
    
    # make a new location for the routing table window
    location = (1200, 100)
    # layout for the routing table window
    layout = [
        [sg.Column(table, background_color='black', key='Table')]
    ]

    # creating a window to display the routing table
    window1 = sg.Window('Routing tables',location=location).Layout(layout)
    # showing the window
    window1.read()

# Inputs: none
# Outputs: none
# Purpose: To find the next node in the shortest path from the dest node to the source node
def find_routing_tables():
    # for each node in the network
    for src in nodes:
        # list to hold the path from the source node to the dest node
        path = []
        # find the path from the source node to each other node
        for dest in nodes:
            # if the source is not the same as the destination 
            if src != dest:
                # try to find a path between the source node and destination node
                try:
                    # Link below was referred to for using the networkx shortest_path function
                    # https://networkx.org/documentation/stable/reference/algorithms/shortest_paths.html
                    curr_path = nx.shortest_path(graph, source=src, target=dest, weight='weight')
                    # append the shortest path to the path list
                    path.append(curr_path)
                # if there was no path found
                except:
                    # insert zero to indicate no path exists between the source node and dest node
                    path.insert(dest-1,[0])
            else:
                # insert zero when the source and dest nodes are the same
                path.insert(dest-1, [0])
        # insert the list of paths into the routing table list
        routing_table.insert(dest-1, path)

# Inputs: none
# Outputs: none
# Purpose: Creates the graph based on the information in the edges list, also saves an .png file of this graph
def create_graph():
    # if a graph image already exists, clear/remove the global variables to avoid leftover information from the previous graph
    if os.path.exists("graph.png"):
        routing_table.clear()
        all_dist.clear()
        graph.clear()
        routing_table.clear()
        nodes.clear()
        os.remove("graph.png")
    
    # Link below referred to for creating a networkx graph from information
    #https://networkx.org/documentation/stable/tutorial.html
    # for each link in the network
    for link in edges:
        # add the edge to the graph
        graph.add_edge(link[0], link[1])
        # add the weight of the edge to the graph
        graph[link[0]][link[1]]['weight'] = link[2]
    
    # find the positions of the nodes of the graph
    pos = nx.spring_layout(graph)
    # Link below referred to for plotting the graph information
    #https://stackoverflow.com/questions/28372127/add-edge-weights-to-plot-output-in-networkx/28372251
    nx.draw(graph, pos, with_labels = True)
    # creating labels so the edge weights will be visible
    labels = nx.get_edge_attributes(graph,'weight')
    # draw the labels onto the graph
    nx.draw_networkx_edge_labels(graph,pos,edge_labels=labels, arrowsize = 20, arrowstyle = 'fancy')

    # for each node in the network
    for i in range(len(graph.nodes)):
        # append the number to the nodes list 
        nodes.append(i+1)
        # create an initial table to initialize the all_dist list to use later for finding the DVR table
        initial_table = [16] * len(graph.nodes)
        # inserting zero where ever the source node = dest node
        initial_table[i] = 0
        # append the initialized list to the all_dist list
        all_dist.append(initial_table)
    
    # saving an .png image of the created graph 
    plt.savefig("graph.png")
    # clearing the plot from the matplotlib
    plt.clf()

# Inputs: file input by the user
# Outputs: boolean if the file read was successful or not
# Purpose: Selects input file from the user and saves the data of all the edges
def select_file(file):
    while True:
        # try except block to catch errors with opening the file
        try:
            # opening the desired file for reading
            fp = open(file, "r")
            while True:
                # list to hold the edge information
                edge = []
                # reading a single line from the file
                line = fp.readline()
                # if file out of lines, break out of infinite loop
                if not line:
                    break
                # spilt the line by spaces
                line = line.split()
                # append the source node to the edge list
                edge.append(int(line[0]))
                # append the dest node to the edge list
                edge.append(int(line[1]))
                # append the weight of the link to the edge list
                edge.append(float(line[2]))
                # append the information to the edges list
                edges.append(edge)
            return True
        # if something went wrong, return false
        except IOError:
            return False

# Inputs: boolean for if the file opened successfully or not, the text file opened, the window for the GUI
# Outputs: the updated window for the GUI
# Purpose: Updating the display on the GUI to show the graph and give the user options of what to do
def show_image(success, text_file, window):
    # if the file was opened successfully
    if success:
        # create the graph
        create_graph()
        # layout for if the text file opened successfully
        layout_textfile = [
            [sg.Text("Enter the text file to read from and press ok"), sg.InputText('', size =(10,1), key='text_file')],
            [sg.Button("Ok")],
            [sg.Text(text_file + " opened successfully")],
            [sg.Image("graph.png"), sg.Button("Routing Tables")],
            [sg.Text("Press single step mode or continous mode to start"), sg.Button("Continous"), sg.Button("Single-Step")],
            [sg.Button("Exit")]
        ]
    else:
        # layout for if the text file failed to open
        layout_textfile = [
            [sg.Text("Enter the text file to read from and press ok"), sg.InputText('', size =(10,1), key='text_file')],
            [sg.Button("Ok")],
            [sg.Text("File did not open successfully, try again")],
            [sg.Button("Exit")]
        ]
    # new window to show the new layout
    window1 = sg.Window("Distance Vector Routing simulation", location=location).Layout(layout_textfile)
    # closing the old window
    window.close()
    # returning the new window
    return window1

# Inputs: none
# Outputs: none
# Purpose: Starts the GUI and happens the events happening in the GUI
def start_GUI():
    # variable to keep track of the old cost of the line when a line goes down
    old_cost = -1
    # variable to keep track of the source node of the line when a line goes down
    changed_N1 = -1
    # variable to keep track of the dest node of the line when a line goes down
    changed_N2 = -1
    # variable to keep track of the number of cycles run in single step mode
    cycle_count = 0
    # variable to keep track of the text file name entered by the user
    text_file = ""
    # variable to keep track if the text file opened successfully or not
    success = False

    # initial layout for the GUI, lets the user input a file
    layout_og = [
        [sg.Text("Enter the text file to read from and press ok"), sg.InputText('', size =(10,1), key='text_file')],
        [sg.Button("Ok")],
        [sg.Button("Exit")]
    ]

    # window to display the layout of the GUI
    window = sg.Window("Distance Vector Routing simulation", location=location).Layout(layout_og)

    # enter an infinite loop until the user wants to exit
    while True:
        # capture the events and values from the window
        event, values = window.read()
        # if the user presses the "Ok" button to enter a text file
        if event == "Ok":
            # clear the edges list in case there are leftover values in it from a previous file
            edges.clear()
            # getting the text file name entered by the user
            text_file = values['text_file']
            # opening the file (or failing to open the file)
            success = select_file(text_file)
            # if the text file opened, create the graph
            if success:
                create_graph()
            # showing the graph image or the error of the text file not opening
            window = show_image(success, text_file, window)
        # if the user presses the "Routing Tables" button 
        elif event == "Routing Tables":
            # find the routing tables for each node
            find_routing_tables()
            # display the routing table window 
            display_routing_tables()
        # if the user presses the "Continous" button
        elif event == "Continous":
            # Run the DVR algorithm in continous mode
            window = DVR_continous(window, False, 0)
        # if the user presses the "Single-step" button
        elif event == "Single-Step":
            # Run the DVR algorithm in single step mode
            window, cycle_count = DVR_singlestep(window, cycle_count)
        # if the user presses the "Reset" button
        elif event == "Reset":
            # reset all the variables to their beginning values
            old_cost = -1
            cycle_count = 0
            edges.clear()
            # rerun the select_file function to re-get the information from the file
            success = select_file(text_file)
            # create the graph from the information from the file
            create_graph()
            # show the graph image
            window = show_image(success, text_file, window)
        # if the user presses the "Change" button
        elif event == "Change":
            # get the source node from the first blank
            node1 = values['node1']
            # get the dest node from the second blank
            node2 = values['node2']
            # get the new link value from the third blank
            new_weight = values['new_weight']
            # if all three blanks have information and the new link value if in the range of [0, 16]
            if node1 and node2 and new_weight and float(new_weight) >= float(0) and float(new_weight) <= float(16):
                # passing the information to the adjust_linkcost function to change the link value
                window, old_cost, changed_N1, changed_N2 = adjust_linkcost(int(node1), int(node2), float(new_weight), window, old_cost, changed_N1, changed_N2)
        # if the user presses the "Exit" button or closes the window
        elif event == "Exit" or event == sg.WIN_CLOSED:
            # break out of the loop
            break
    
    #close the window
    window.close()

if __name__ == "__main__":
    # global variable to save the location of the window
    global location
    location = (500,100)
    # global list to save all the link information
    global edges
    edges = []
    # global list to save the calculated DVR information
    global all_dist
    all_dist = []
    # global list to save the routing tables for each node
    global routing_table
    routing_table = []
    # global variable to save the graph information
    global graph
    graph = nx.DiGraph()
    # global list to save all the nodes in the network
    global nodes
    nodes = []

    # begin the GUI window
    start_GUI()