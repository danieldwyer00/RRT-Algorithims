from shapely.geometry import Polygon, LineString, Point
import matplotlib.pyplot as plt
import random
 
plt.ion()
fig, ax = plt.subplots()
points = ax.scatter([], [], c='b')  # current position



obstacles = [
    Polygon([(1, 0), (2, 0), (2, 3), (1, 3)]),  # square obstacle
    Polygon([(3, 1), (4, 1), (4, 4), (3, 4)]),
    Polygon([(5, 0), (6, 0), (6, 3), (5, 3)])             
]



def plot_obstacles(obstacles):
    for obs in obstacles:
        x, y = obs.exterior.xy
        plt.fill(x, y, color='gray')

plot_obstacles(obstacles)

def Distance(Point1,Point2):
    return ((Point1.position[0]-Point2.position[0])**2 + (Point1.position[1]-Point2.position[1])**2)**0.5

def check_collision(point1, point2, obstacles):
    line = LineString([point1.position, point2.position])
    return any(line.intersects(obs) for obs in obstacles)

class Node:
    def __init__(self, position, atEndNode=False, distanceToParent=None, parent=None):
        self.position = position          # (x, y)
        self.parent = parent              # Parent Node
        self.distanceToParent = distanceToParent
        self.CumulativeLength = 0                   # Accumulated path length
        self.children = []                # Useful for rewiring (optional)
        self.atEndNode = atEndNode
        if parent:
            self.CumulativeLength = parent.CumulativeLength + self.distanceToParent
            parent.children.append(self)

maxStepDistance = 3
endStepDistance = 0.5

StartNode = Node([0,0])
EndNode = Node([7,0])

ax.scatter(StartNode.position[0], StartNode.position[1], c='blue', s=100, label="Start")
ax.scatter(EndNode.position[0], EndNode.position[1], c='green', s=100, label="Goal")

Nodes = [
    StartNode
]

shortest_path_lines = []

foundSolution = False

while True:
    #Generate Random Node
    random_x = random.uniform(0,7)
    random_y = random.uniform(0,4)

    #Create temp Node
    tempNode = Node([random_x,random_y])

    #Find Nearest Existing Node
    tempNearestDistance = 999999999
    for node in Nodes:
        if Distance(node,tempNode) < tempNearestDistance:
            NearestNode = node
            tempNearestDistance = Distance(node,tempNode)
            tempNode = Node([random_x,random_y],False,tempNearestDistance,NearestNode)
        
    #Append to Node List if within max distance and no collision
    
    if tempNearestDistance <= maxStepDistance and check_collision(tempNode,tempNode.parent,obstacles) == False:
        if Distance(EndNode,tempNode) <= endStepDistance:
            tempNode.atEndNode = True
        Nodes.append(tempNode)
        ax.plot([Nodes[-1].position[0],Nodes[-1].parent.position[0]],[Nodes[-1].position[1],Nodes[-1].parent.position[1]],'r',lw = 1)
        plt.pause(0.05)

    #Find Current Shortest Branch
    ShortestCumulativeLength = 999999999
    for node in Nodes:
        if node.atEndNode == True:
            if node.CumulativeLength < ShortestCumulativeLength:
                ShortestCumulativeLength = node.CumulativeLength
                ShortestBranchNode = node
                foundSolution = True
    #print("Shortest Distance: " + str(ShortestCumulativeLength))

    if foundSolution == True:
        # Clear previous shortest path
        for line in shortest_path_lines:
            line.remove()
        shortest_path_lines.clear()

        # Backtrack and plot new shortest path in green
        current = ShortestBranchNode
        while current.parent is not None:
            line, = ax.plot(
                [current.position[0], current.parent.position[0]],
                [current.position[1], current.parent.position[1]],
                'g', lw=2
            )
            shortest_path_lines.append(line)
            current = current.parent