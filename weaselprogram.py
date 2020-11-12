import numpy as np
from randomgen import PCG64
import itertools
import time

gene_bases = [base for base in " ABCDEFGHIJKLMNOPQRSTUVWXYZ"]

seed = 1
size_of_generation = 1000

prngs = [np.random.Generator(PCG64(seed, i)) for i in range(size_of_generation)]


def mutate(prng, gene, mutation_rate=0.05):
    return "".join(
        prng.choice(gene_bases) if prng.random() < mutation_rate else base
        for base in gene
    )


def fitness(gene, reference="METHINKS IT IS LIKE A WEASEL"):
    return sum(base == ref_base for base, ref_base in zip(gene, reference))


def print_status(gen, parent, score):
    print(f"{gen:3d}  {parent}  ({score})")


def weasel_program(mutation_rate=0.05, initial="                            "):
    generation = 0
    score = fitness(initial)
    parent = initial
    while score < len(parent):
        print_status(generation, parent, score)
        parent = max(
            [mutate(prng, parent, mutation_rate=mutation_rate) for prng in prngs],
            key=fitness,
        )
        generation += 1
        score = fitness(parent)
    print_status(generation, parent, score)


start_time = time.perf_counter()
weasel_program()
stop_time = time.perf_counter()
print(f"evolution time: {stop_time - start_time}s")
