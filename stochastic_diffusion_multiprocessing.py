import matplotlib.pyplot as plt
import time
import random
import sys
import plotnine as p9
import pandas as pd
import multiprocessing
import itertools

x_lo = 0
x_hi = 200
num_molecules = 100_000
PLOT_EVERY = 400

try:
    NUM_PROCESSES = int(sys.argv[1])
except:
    print(f"Run via: python {sys.argv[0]} NUM_PROCESSES")
    sys.exit(-1)

# our rule for diffusion
def advance(args):
    molecules, tsteps = args
    for i, mol_loc in enumerate(molecules):
        for _ in range(tsteps):
            r = random.random()
            if r < 0.4:
                mol_loc = max(x_lo, mol_loc - 1)
            elif r < 0.8:
                mol_loc = min(x_hi, mol_loc + 1)
        molecules[i] = mol_loc
    return molecules


def partition(n, m):
    """split 0 through n into m groups differing by at most 1

    Assumes end point is not included
    """
    remainder = n % m
    per_each = n // m
    # the first remainder get an extra 1
    first_part = [
        (i * (per_each + 1), (i + 1) * (per_each + 1)) for i in range(remainder)
    ]
    start = remainder * (per_each + 1)
    second_part = [
        (i * per_each + start, (i + 1) * per_each + start) for i in range(m - remainder)
    ]
    return first_part + second_part


def plot_it(molecules, t):
    counts = [0] * (x_hi - x_lo + 1)
    for mol_loc in molecules:
        counts[mol_loc] += 1
    data = pd.DataFrame({"x": range(x_lo, x_hi + 1), "t": t, "count": counts})
    return p9.geom_line(data=data, size=1)


if __name__ == "__main__":
    molecule_locations = [100] * num_molecules

    my_plot = p9.ggplot(p9.aes(x="x", y="count", color="t"))
    start = time.perf_counter()
    intervals = partition(num_molecules, NUM_PROCESSES)
    with multiprocessing.Pool(NUM_PROCESSES) as pool:
        for t in range(0, 2001, PLOT_EVERY):
            my_plot += plot_it(molecule_locations, f"{t} ms")
            mol_parts = [molecule_locations[i[0] : i[1]] for i in intervals]
            molecule_locations = list(
                itertools.chain.from_iterable(
                    pool.map(advance, [(mols, PLOT_EVERY) for mols in mol_parts])
                )
            )
    if t % PLOT_EVERY == 0:
        my_plot += plot_it(molecule_locations, f"{t} ms")
    stop = time.perf_counter()

    print(f"simulation time: {stop - start}")
    my_plot += p9.scale_y_continuous(limits=(0, 3_000))
    my_plot.draw()
    plt.show()
