from colorama import Fore, Style
from os import system, name
from time import sleep

speed = 0.005


def clear():
  if name == 'nt':
    _ = system('cls')
  else:
    _ = system('clear')

def PrintMaze(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == "O":
                print(Fore.YELLOW + maze[i][j], end="")
                print(Style.RESET_ALL, end="")
            elif maze[i][j] != "S" and maze[i][j] != "F":
                print(maze[i][j], end="")
            else:
                print(Fore.BLUE + maze[i][j], end="")
                print(Style.RESET_ALL, end="")
        print()
    sleep(speed)
    clear()


def printPath(maze, path, start, end, name_search):
    count_visited = 0
    count_route = 0
    for k in reversed(path):
        if k != start and k != end:
            maze[int(k[0])][int(k[1])] = "#"
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                if maze[i][j] == "O":
                    if k == path[0]:
                        count_visited += 1
                    print(Fore.YELLOW + maze[i][j], end="")
                    print(Style.RESET_ALL, end="")
                elif maze[i][j] == "#":
                    if k == path[0]:
                        count_route += 1
                    print(Fore.RED + maze[i][j], end="")
                    print(Style.RESET_ALL, end="")

                elif maze[i][j] != "S" or maze[i][j] != "F":
                    print(maze[i][j], end="")
                else:
                    print(Fore.BLUE + maze[i][j], end="")
                    print(Style.RESET_ALL, end="")
            print()

        sleep(speed*2)
        if k != path[0]:
            clear()
    print("S - Start\nF - Final\nO - Opened node\n# - Path\nX - Wall\nSpace - Fresh node\n------------------")
    print(name_search + ":")
    print("Nodes expanded: " + str(count_visited + count_route + 1))
    print("Path length:" + str(count_route + 1))
    print("------------------\n")


def ClearMatrix(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if (maze[i][j] == "O"):
                maze[i][j] = " "
            if (maze[i][j] == "#"):
                maze[i][j] = " "
    return maze