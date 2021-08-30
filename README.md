# DVR-algo

DVR.py requires a few different python libraries. These libraries are networkx,
matplotlib, and pysimplegui. To download all of these I used pip install networkx, pip
install matplotlib, and pip install pysimplegui in the Anaconda3 prompt. The installing
instructions for all three of these libraries are linked below.
https://pypi.org/project/networkx/
https://matplotlib.org/stable/users/installing.html
https://pypi.org/project/PySimpleGUI/
After unzipping the directory, navigate to inside the folder and run make. For whatever
reason if the makefile does not work, use the command python DVR.py in the project
directory. Since I installed the libraries through anaconda, I ran the program through the
anaconda prompt and it worked well.
About the program:
Text Input
When the GUI first starts, you will see an input box for the text file. Input the text file and
press the Ok button. If the text file does not open successfully, the GUI will let the user
know and let the user try again. After entering a valid text file, a network graph will
appear along with several options. A button to the right of the network graph will pull up
a separate window with the routing tables for each node. Different text files can be
entered after the initial text file is entered.
Routing Tables
The left column of the table is a list of the destination nodes and the right column is the
next node to go to in the shortest path for each source node. The tables for each node
are separated by a header labeled as “Dest nodes, Next node from source node: #” with
the number being the node the routing table is for. If there is not a path between the
source node and destination node, “None” will be the value. The routing table does not
show the closest node for when the source node and dest node are the same because
it would be just the same node. The routing tables window must be closed before
anything else can be done in the main window.
Continuous and Single-Step mode
Press the Continuous button to start the continuous mode. After pressing this button,
the Distance Vector Routing table will appear. The Distance Vector Routing table is
meant to be read left to right with the first column being the source nodes and the first
row being the destination nodes. Each row after the first row is the distance to each
destination node from the denoted source node. For example, if you are trying to find
the shortest distance from node 1 to node 5, the distance would be at the intersection of
the second row and sixth column. If the value is 16, this means a path does not exist
between the source and destination node. The single-step mode will run one cycle at a
time with each cycle finding the distance vector information for each node. After the
network has reached a stable state, the DVR table will no longer change (unless a link
is changed) or the reset button is pressed. Press the reset button to clear the DVR table
and re-run continuous or single-step mode, note any changes made to the links will also
be reset to what it was originally from the text file.
Changing a link cost
To change the link cost, input the source node in the first input box, the destination node
in the second input box and the new weight for the link in the third input box and press
the Change button. If a link that does not exist in the network is entered, nothing will
happen when the Change button is pressed. Also if an invalid weight is entered, which
is any weight less than 0 or greater than 16, nothing will happen either. If the new
weight is 16, a line will be “down”. In order to repair the line, the same source node,
destination node and previous weight for that link must be entered in order to proceed.
Attempting to change any other links during a line being down will not work. After
entering the correct nodes and weight and pressing change, the window will return to
normal. Changing the link normally for any link will then run continuous mode
automatically and the DVR table and routing tables will be changed. If the Reset button
is pressed, all changes to the links will be reset to the original costs.
Limitations
The GUI can be a bit slow at times. Just give it a minute and it will load but sometimes it
may freeze and crash. Just rerun the program if it crashes. Sometimes the network
graph will be formatted weirdly. The data is right, you can verify this by looking at the
routing tables the graph just comes out weird sometimes. As noted previously, the
routing tables window must be closed before doing anything else in the main GUI.
