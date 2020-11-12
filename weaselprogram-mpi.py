import numpy as np
from randomgen import PCG64
import itertools
import time
from mpi4py import MPI

communicator = MPI.COMM_WORLD
rank = communicator.rank
nnode = communicator.size


gene_bases = [base for base in " ABCDEFGHIJKLMNOPQRSTUVWXYZ"]

seed = 1
size_of_generation = 1000

num_each = size_of_generation // nnode

start = num_each * rank
stop = num_each * (rank + 1)
if rank == nnode - 1:
    stop = size_of_generation

prngs = [np.random.Generator(PCG64(seed, i)) for i in range(start, stop)]


def mutate(prng, gene, mutation_rate=0.05):
    return "".join(
        prng.choice(gene_bases) if prng.random() < mutation_rate else base
        for base in gene
    )


def fitness(gene, reference="METHINKS IT IS LIKE A WEASEL"):
    return sum(base == ref_base for base, ref_base in zip(gene, reference))


def print_status(gen, parent, score):
    if not rank:
        print(f"{gen:3d}  {parent}  ({score})")


def new_population(parent, mutation_rate=0.05):
    return [
        mutate(prng, parent, mutation_rate=mutation_rate) for prng in prngs[start:stop]
    ]


def best_in_population(population):
    """return the fittest individual in the population"""
    return max(population, key=fitness)


def weasel_program(mutation_rate=0.05, initial="                            "):
    generation = 0
    score = fitness(initial)
    parent = initial
    while score < len(parent):
        print_status(generation, parent, score)
        possible_parents = list(
            itertools.chain.from_iterable(
                communicator.allgather(
                    new_population(parent, mutation_rate=mutation_rate)
                )
            )
        )
        parent = best_in_population(possible_parents)
        generation += 1
        score = fitness(parent)
    print_status(generation, parent, score)


start_time = time.perf_counter()
weasel_program()
stop_time = time.perf_counter()
if not rank:
    print(f"evolution time: {stop_time - start_time}s")
