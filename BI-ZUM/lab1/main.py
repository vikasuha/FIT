import algorithms
import PrintMaze

FileName = "01_71_51_156.txt"
PathToFile = "dataset/" + FileName


def main():

    tmp = ReadFile()
    matrix = tmp[0]
    start_point = tmp[1]
    end_point = tmp[2]
    while True:
        choice = ReadInput()
        if choice == '1':
            algorithms.RandomSearch(matrix, start_point, end_point)
        elif choice == '2':
            algorithms.DFS(matrix, start_point, end_point)
        elif choice == '3':
            algorithms.BFS(matrix, start_point, end_point)
        elif choice == '4':
            algorithms.GreedSearch(matrix, start_point, end_point)
        elif choice == '5':
            algorithms.Dijkstra(matrix, start_point, end_point)
        elif choice == '6':
            algorithms.AStar(matrix, start_point, end_point)
        elif choice == '7':
            break
        matrix = PrintMaze.ClearMatrix(matrix)



def ReadFile():
    f = open(PathToFile).readlines()
    tmp = list()
    with open(PathToFile) as file:
        for line in file:
            tmp.append(list(line.rstrip()))
    matrix = tmp[:-2]
    tmp = [line.replace("\n", "") for line in f]
    start_line = tmp[-2].split(" ")
    start_point = (int(start_line[2]), int(start_line[1][:-1]))
    end_line = tmp[-1].split(" ")
    end_point = (int(end_line[2]), int(end_line[1][:-1]))
    matrix[int(start_point[0])][int(start_point[1])] = "S"
    matrix[int(end_point[0])][int(end_point[1])] = "F"
    return matrix, start_point, end_point


def ReadInput():
    print(" [1] - Random Search \n"
          " [2] - DFS\n"
          " [3] - BFS\n"
          " [4] - Greedy Search\n"
          " [5] - Dijkstra\n"
          " [6] - A*\n"
          " [7] - Exit\n")
    choice = input("Enter algorithm number: ")
    return choice

if __name__=="__main__":
    main()