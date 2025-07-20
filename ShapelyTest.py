from shapely.geometry import Polygon, LineString, Point
import matplotlib.pyplot as plt

obstacles = [
    Polygon([(2, 2), (4, 2), (4, 4), (2, 4)]),  # square obstacle
    Polygon([(6, 1), (7, 3), (5, 2)])           # triangle obstacle
]
point1 = [0,0]
point2 = [4.5,3.5]

def plot_obstacles(obstacles):
    for obs in obstacles:
        x, y = obs.exterior.xy
        plt.fill(x, y, color='gray')

def plot_points(p1, p2):
    plt.scatter([p1[0], p2[0]], [p1[1], p2[1]], color='blue')
    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color='red')

def check_collision(point1, point2, obstacles):
    line = LineString([point1, point2])
    return any(line.intersects(obs) for obs in obstacles)

plot_obstacles(obstacles)
plot_points(point1,point2)
if check_collision(point1,point2,obstacles):
    print("Collision Detected")

plt.show()