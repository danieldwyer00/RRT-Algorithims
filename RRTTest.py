from shapely.geometry import Polygon, LineString, Point
import matplotlib.pyplot as plt
import random
 
plt.ion()
fig, ax = plt.subplots()
points = ax.scatter([], [], c='b')  # current position



obstacles = [
    Polygon([(2, 2), (4, 2), (4, 4), (2, 4)]),  # square obstacle
    Polygon([(6, 1), (7, 3), (5, 2)])           # triangle obstacle
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
    def __init__(self, position, distanceToParent=None, parent=None):
        self.position = position          # (x, y)
        self.parent = parent              # Parent Node
        self.distanceToParent = distanceToParent
        self.CumulativeLength = 0                   # Accumulated path length
        self.children = []                # Useful for rewiring (optional)
        
        if parent:
            self.CumulativeLength = parent.CumulativeLength + self.distanceToParent
            parent.children.append(self)


Nodes = [
    Node([0,0]),
    Node([0,0])
]


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
            tempNode = Node([random_x,random_y],tempNearestDistance,NearestNode)

    #Append to Node List if within max distance and no collision
    maxDistance = 1
    if tempNearestDistance <= maxDistance and check_collision(tempNode,tempNode.parent,obstacles) == False:
        Nodes.append(tempNode)
        ax.plot([Nodes[-1].position[0],Nodes[-1].parent.position[0]],[Nodes[-1].position[1],Nodes[-1].parent.position[1]],'r')
        plt.pause(0.05)

    

    

