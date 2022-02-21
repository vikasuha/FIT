#Viktoriia Sukha
#sukhavik
import os
import sys
import numpy
import matplotlib.pyplot
import itertools
import functools
import operator
import random
from PIL import Image
from pip._vendor.distlib.compat import raw_input
import imageio


def initial_population(img_shape, n_individuals=8):
    init_population = numpy.empty((n_individuals, functools.reduce(operator.mul, img_shape)), numpy.uint8)
    for indv_num in range(n_individuals):
        init_population[indv_num, :] = numpy.random.random(
            functools.reduce(operator.mul, img_shape)) * 256
    return init_population



def count_fitness(target_chrom, indiv_chrom):
    quality = numpy.mean(numpy.abs(target_chrom - indiv_chrom))
    quality = numpy.sum(target_chrom) - quality
    return quality


def get_fitness(target_chrom, pop):
    qualities = numpy.zeros(pop.shape[0])
    for indv_num in range(pop.shape[0]):
        qualities[indv_num] = count_fitness(target_chrom, pop[indv_num, :])
    return qualities


def select_parents(pop, qualities, num_parents):
    parents = numpy.empty((num_parents, pop.shape[1]), numpy.uint8)
    for parent_num in range(num_parents):
        max_qual_idx = numpy.where(qualities == numpy.max(qualities))
        max_qual_idx = max_qual_idx[0][0]
        parents[parent_num, :] = pop[max_qual_idx, :]
        qualities[max_qual_idx] = -1
    return parents



def redo_img_to_chrom(img_arr):
    chromosome = numpy.reshape(img_arr, (functools.reduce(operator.mul, img_arr.shape)))
    return chromosome



def redo_chrom_to_img(chromosome, img_shape):
    img_arr = numpy.reshape(chromosome, img_shape)
    return img_arr




def crossover(parents, img_shape, n_individuals=8):
    new_population = numpy.empty((n_individuals, functools.reduce(operator.mul, img_shape)), numpy.uint8)

    new_population[0:parents.shape[0], :] = parents
    num_newly_generated = n_individuals - parents.shape[0]
    parents_permutations = list(itertools.permutations(numpy.arange(0, parents.shape[0]), r=2))
    selected_permutations = random.sample(range(len(parents_permutations)), num_newly_generated)

    comb_idx = parents.shape[0]
    for comb in range(len(selected_permutations)):
        selected_comb_idx = selected_permutations[comb]
        selected_comb = parents_permutations[selected_comb_idx]
        half_size = numpy.int32(new_population.shape[1] / 2)
        new_population[comb_idx + comb, 0:half_size] = parents[selected_comb[0], 0:half_size]
        new_population[comb_idx + comb, half_size:] = parents[selected_comb[1], half_size:]

    return new_population


def mutation(population, num_parents_mating, mut_percent):
    for idx in range(num_parents_mating, population.shape[0]):
        rand_idx = numpy.uint32(numpy.random.random(numpy.uint32(mut_percent / 100 * population.shape[1])) * population.shape[1])
        new_values = numpy.uint8(numpy.random.random(rand_idx.shape[0]) * 256)
        population[idx, rand_idx] = new_values
    return population


def save_images(curr_iteration, qualities, new_population, im_shape, save_point, save_dir):
    if (numpy.mod(curr_iteration, save_point) == 0):
        best_solution_chrom = new_population[numpy.where(qualities == numpy.max(qualities))[0][0], :]
        best_solution_img = redo_chrom_to_img(best_solution_chrom, im_shape)
        matplotlib.pyplot.imsave(save_dir + 'solution_' + str(curr_iteration) + '.png', best_solution_img)




def main():
    sol_per_pop = 32
    num_parents_mating = 16
    mutation_percent = 0.01
    num_of_iteration = 20000
    image_name = 'apple.jpg'
    while (True):
        print("[1] - change number of iteration ( cur " + str(num_of_iteration) + " )\n"
              "[2] - change population size ( cur " + str(sol_per_pop) + " )\n"
              "[3] - change mutation percentage ( cur " + str(mutation_percent) + ")\n"
              "[4] - run algorithm\n"
              "[5] - exit")
        choise = raw_input("Please Select:")
        if choise == "1":
            num_of_iteration = int(raw_input("Enter new number of iteration:"))
        elif choise == "2":
            sol_per_pop = int(raw_input("Enter new population size:"))
            num_parents_mating = sol_per_pop/2
        elif choise == "3":
            mutation_percent = int(raw_input("Enter new mutation percentage:"))
        elif choise == "4":
            break
        elif choise == "5":
            exit(0)
        else:
            print("Wrong input, try again.\n")


    target_im = imageio.imread(image_name)
    target_chromosome = redo_img_to_chrom(target_im)

    new_population = initial_population(target_im.shape, sol_per_pop)
    print("Wait a while")
    for iteration in range(num_of_iteration+1):
        qualities = get_fitness(target_chromosome, new_population)
        parents = select_parents(new_population, qualities, num_parents_mating)
        new_population = crossover(parents, target_im.shape, sol_per_pop)
        new_population = mutation(new_population, num_parents_mating, mutation_percent)
        save_images(iteration, qualities, new_population, target_im.shape, 5000, os.curdir + '//')
        if iteration % 5000 == 0:
            im0 = Image.open('solution_' + str(iteration) + '.png')
            im0.show()
            im0.close()

    im1 = Image.open("apple.jpg")
    im1.show()
    last_img = num_of_iteration - num_of_iteration % 5000
    im = Image.open('solution_' + str(last_img) + '.png')
    im.show()

if __name__ == "__main__":
    main()