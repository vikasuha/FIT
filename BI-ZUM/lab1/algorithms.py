from colorama import Fore, Style
from os import system, name
from time import sleep

import PrintMaze
import random
from queue import PriorityQueue


def RandomSearch(maze, start, end):
    queue = [start]
    visited = set()
    while len(queue) != 0:
        if queue[0] == start:
            path = [queue.pop(0)]
        else:
            path = random.choice(queue)
        front = path[-1]
        if front == end:
            PrintMaze.printPath(maze, path, start, end, "Random Search")
            return
        elif front not in visited:
            for adjacentSpace in getAdjacentSpaces(maze, front, visited):
                newPath = list(path)
                newPath.append(adjacentSpace)
                queue.append(newPath)
            visited.add(front)
            for point in visited:
                if point != start and point != end:
                    maze[int(point[0])][int(point[1])] = "O"
            PrintMaze.PrintMaze(maze)
    PrintMaze("No path to destination.")


def DFS(maze, start, end):
    visited = set()
    stack = []
    stack.append([start])
    while len(stack) != 0:
        path = stack.pop()
        front = path[-1]
        if front == end:
            PrintMaze.printPath(maze, path, start, end, "DFS")
            return
        elif front not in visited:
            for adjacentSpace in getAdjacentSpaces(maze, front, visited):
                newPath = list(path)
                newPath.append(adjacentSpace)
                stack.append(newPath)
            visited.add(front)
            for point in visited:
                if point != start and point != end:
                    maze[int(point[0])][int(point[1])] = "O"
            PrintMaze.PrintMaze(maze)
        print("No path to destination.")


def BFS(maze, start, end):
    queue = [start]
    visited = set()
    while len(queue) != 0:
        if queue[0] == start:
            path = [queue.pop(0)]
        else:
            path = queue.pop(0)
        front = path[-1]
        if front == end:
            PrintMaze.printPath(maze, path, start, end, "BFS")
            return
        elif front not in visited:
            for adjacentSpace in getAdjacentSpaces(maze, front, visited):
                newPath = list(path)
                newPath.append(adjacentSpace)
                queue.append(newPath)
            visited.add(front)
            for point in visited:
                if point != start and point != end:
                    maze[int(point[0])][int(point[1])] = "O"
            PrintMaze.PrintMaze(maze)
    print("No path to destination.")


def Dijkstra(maze, start, end):
    queue = PriorityQueue()
    queue.put((0, start))
    visited = set()
    while queue:
        cur = queue.get()
        if cur[1] == start:
            path = [cur[1]]
        else:
            path = cur[1]
        front = path[-1]
        if front == end:
            PrintMaze.printPath(maze, path, start, end, "Dijkstra")
            return
        elif front not in visited:
            for adjacentSpace in getAdjacentSpaces(maze, front, visited):
                newPath = list(path)
                newPath.append(adjacentSpace)
                queue.put((cur[0] + 1, newPath))
            visited.add(front)
            for point in visited:
                if point != start and point != end:
                    maze[int(point[0])][int(point[1])] = "O"
            PrintMaze.PrintMaze(maze)
    print("No path to destination.")


def GreedSearch(maze, start, end):
    queue = PriorityQueue()
    queue.put((0, start))
    visited = set()
    while queue:
        cur = queue.get()
        if cur[1] == start:
            path = [cur[1]]
        else:
            path = cur[1]
        front = path[-1]
        if front == end:
            PrintMaze.printPath(maze, path, start, end, "Greedy Search")
            return
        elif front not in visited:
            for adjacentSpace in getAdjacentSpaces(maze, front, visited):
                newPath = list(path)
                newPath.append(adjacentSpace)
                dist = pow((pow(abs(end[0] - adjacentSpace[0]), 2) + pow(abs(end[1] - adjacentSpace[1]), 2)), 0.5)
                queue.put((dist, newPath))
            visited.add(front)
            for point in visited:
                if point != start and point != end:
                    maze[int(point[0])][int(point[1])] = "O"
            PrintMaze.PrintMaze(maze)
    print("No path to destination.")


def AStar(maze, start, end):
    queue = PriorityQueue()
    queue.put((0, start, 0))
    visited = set()
    while queue:
        cur = queue.get()
        if cur[1] == start:
            path = [cur[1]]
        else:
            path = cur[1]
        front = path[-1]
        if front == end:
            PrintMaze.printPath(maze, path, start, end, "A*")
            return
        elif front not in visited:
            for adjacentSpace in getAdjacentSpaces(maze, front, visited):
                newPath = list(path)
                newPath.append(adjacentSpace)
                dist = pow((pow(abs(end[0] - adjacentSpace[0]), 2) + pow(abs(end[1] - adjacentSpace[1]), 2)), 0.5)
                queue.put((dist + cur[2] + 1, newPath, cur[2] + 1))
            visited.add(front)
            for point in visited:
                if point != start and point != end:
                    maze[int(point[0])][int(point[1])] = "O"
            PrintMaze.PrintMaze(maze)
    print("No path to destination.")


def getAdjacentSpaces(maze, space, visited):
    spaces = list()
    spaces.append((space[0] - 1, space[1]))  # Up
    spaces.append((space[0] + 1, space[1]))  # Down
    spaces.append((space[0], space[1] - 1))  # Left
    spaces.append((space[0], space[1] + 1))  # Right
    final = list()
    for i in spaces:
        if maze[i[0]][i[1]] != 'X' and i not in visited:
            final.append(i)
    return final
