import os

import rtree
import tests
from rect import Rect
from tests.test_rtree import TstO


from my_tree import my_tree

def FindData(tree):
    x = input("Enter coordinate x (in format 0.0): ")
    y = input("Enter coordinate y (in format 0.0): ")
    tree.FindPoint(float(x), float(y))

def AddData(tree):
    x = input("Enter coordinate x (in format 0.0): ")
    y = input("Enter coordinate y (in format 0.0): ")
    tree.AddData(float(x), float(y))

def OperationWithTree(tree):
    visual = False
    while True:
        print("[1] - save tree")
        print("[2] - add data")
        # print("[3] - find data")
        print("[3] - show tree")
        if not tree.visual:
            print("[4] - turn on printing coordinates of rectangles")
        else:
            print("[4] - turn off printing coordinates of rectangles")
        print("[5] - to main menu")

        choice = input("Enter number: ")
        if choice == '1':
            file_name = input("Enter name of file: ")
            tree.SaveTree(file_name)
        elif choice == '2':
            AddData(tree)
        # elif choice =='3':
        #     FindData(tree)
        elif choice == '3':
            tree.invariants(tree.rt)
        elif choice == '4':
            tree.visual = not tree.visual
        elif choice == '5':
            break



def main():
    visual = False
    while True:
        print("Welcome to building an R-tree!")
        print("Select one of the following: ")
        print("[1] - generate random tree")
        print("[2] - build a tree manually")
        print("[3] - load existing tree")
        if not visual:
            print("[4] - turn on printing coordinates of rectangles")
        else:
            print("[4] - turn off printing coordinates of rectangles")
        print("[5] - Exit")

        choice = input("Enter number: ")


        if choice == '1':
            print("Enter number of elements in tree")
            num_of_elements = input("Enter number: ")
            tree = my_tree()
            tree.visual = visual
            tree.BuildTree(int(num_of_elements))
            OperationWithTree(tree)
            # maybe enter size of "point"
        elif choice == '2':
            tree = my_tree()
            tree.visual = visual
            OperationWithTree(tree)

        elif choice == '3':
            files = [f for f in os.listdir(os.curdir) if os.path.isfile(f)]
            i = 0
            print("Choose file:")
            for f in files:
                if f.startswith("rt_"):
                    print(f)

            file_name = input("Enter name of file: ")
            tree = my_tree()
            tree.visual = visual
            tree.LoadTree(file_name)
            OperationWithTree(tree)
            # print("Choose one of this file:")
        elif choice == '4':
            visual = not visual
        elif choice == '5':
            break



if __name__ == '__main__':
    main()
