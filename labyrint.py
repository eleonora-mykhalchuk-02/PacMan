import random
import numpy as np

def generateMaze(width,height):
    maze = []
    visited = []
    for i in range(height):
        maze.append([])
        visited.append([])
        for j in range(width):
            visited[-1].append(0)
            maze[-1].append(0)

    startX = random.randint(0,height - 1)
    startY = random.randint(0,width - 1)
    queue = []

    maze[startX][startY] = 0

    DFSGo(startX,startY,startX,startY,visited,queue,maze)

    return(maze)

#DFS algorithm
def DFSGo(betwX,betwY,startX,startY,visited,queue,maze):
    queue, visited
    if startX < 0 or startY < 0 or startX > len(visited)-1 or startY > len(visited[0])-1:
        return
    if (startX, startY) in queue or visited[startX][startY] > 0:
        return
    queue.append((startX, startY))
    visited[startX][startY] = 1
    visited[betwX][betwY] = 1
    maze[startX][startY] = 1
    maze[betwX][betwY] = 1

    randomWayArr = [0,1,2,3]
    np.random.shuffle(randomWayArr)

    for item in randomWayArr:
        if item == 0:
            DFSGo(startX - 1, startY,startX - 2, startY,visited,queue,maze)  # up
        if item == 1:
            DFSGo(startX + 1, startY,startX + 2, startY,visited,queue,maze)  # down
        if item == 2:
            DFSGo(startX, startY + 1,startX, startY + 2,visited,queue,maze)  # right
        if item == 3:
            DFSGo(startX, startY - 1,startX, startY - 2,visited,queue,maze)  # left

    queue.pop()
    return maze.copy()