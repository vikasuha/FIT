import os

import gen_alg
import game

def main():
    while True:
        Anim = False
        print("Welcome to snake game:")
        print("Select one of the following: ")
        print("[1] - start training snakes and save the best")
        print("[2] - start game with snakes saved previously")
        print("[3] - exit")

        choice = input("Enter number: ")
        if choice == '1':
            file_name = input("Enter name for output file: ")
            gen_alg.main(file_name+'.pickle')
            print("Run genetic algorithm")
        elif choice == '2':
            path = os.getcwd() + "/saved"
            print(os.listdir(path))
            files = [f for f in os.listdir(path)]
            i = 0
            print("Select file:")
            for f in files:
                i = i+1
                print("[" + str(i) + "]" + " - " + str(f))
            file_num = input("Enter number: ")
            file_name = files[int(file_num)-1]
            game.main(file_name)
        elif choice == '3':
            break


if __name__ == '__main__':
    main()





