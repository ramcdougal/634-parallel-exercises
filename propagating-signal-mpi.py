import matplotlib.pyplot as plt
import pandas as pd
import plotnine as p9
import time
from mpi4py import MPI
import itertools

communicator = MPI.COMM_WORLD
rank = communicator.rank
nnode = communicator.size

# initial conditions
y = [0] * 1000
y[480:520] = [1] * 40

# time-step
dt = 0.01


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


all_partitions = partition(len(y), nnode)
start, stop = all_partitions[rank]

# our rule for reaction-diffusion
def advance(dt, y):
    n = len(y)
    new_y = list(y)
    for j in range(start, stop):
        new_y[j] += dt * (
            20 * (y[j - 1] - 2 * y[j] + y[(j + 1) % n])
            - y[j] * (1 - y[j]) * (0.3 - y[j])
        )
    return new_y


def plot_it(t, concentration):
    data = pd.DataFrame(
        {"x": range(len(y)), "t": f"t={t}", "concentration": concentration}
    )
    return p9.geom_line(data=data, size=1)


if __name__ == "__main__":
    my_plot = p9.ggplot(p9.aes(x="x", y="concentration", color="t"))
    start_time = time.perf_counter()

    # advance through t=100, plot
    # every 20
    for i in range(int(100 / dt)):
        t = i * dt

        if t % 20 == 0:
            # everybody sends their part, and ends up with the whole vector
            y = list(
                itertools.chain.from_iterable(communicator.allgather(y[start:stop]))
            )
            if rank == 0:
                my_plot += plot_it(t, y)

        y = advance(dt, y)
        # only need to share the boundary nodes, because that's the only place
        # diffusion can happen from
        boundary_nodes = communicator.allgather((y[start], y[stop - 1]))

        for (i, j), vals in zip(all_partitions, boundary_nodes):
            y[i], y[j - 1] = vals

    stop_time = time.perf_counter()
    if rank == 0:
        print(f"elapsed time: {stop_time - start_time} s")

        my_plot.draw()
        plt.show()
