import matplotlib.pyplot as plt
import time
import random
import plotnine as p9
import pandas as pd

x_lo = 0
x_hi = 200
num_molecules = 100_000
molecule_locations = [100] * num_molecules

# our rule for diffusion
def advance(molecules):
    for i, mol_loc in enumerate(molecules):
        r = random.random()
        if r < 0.4:
            molecules[i] = max(x_lo, mol_loc - 1)
        elif r < 0.8:
            molecules[i] = min(x_hi, mol_loc + 1)

def plot_it(molecules, t):
    counts = [0] * (x_hi - x_lo + 1)
    for mol_loc in molecules:
        counts[mol_loc] += 1
    data = pd.DataFrame({
            'x': range(x_lo, x_hi + 1),
            't': t,
            'count': counts
    })
    return p9.geom_line(data=data, size=1)

if __name__ == '__main__':
    my_plot = p9.ggplot(p9.aes(x='x', y='count', color='t'))
    start = time.perf_counter()
    for t in range(2001):
        if t % 400 == 0:
            my_plot += plot_it(molecule_locations, f'{t} ms')
        advance(molecule_locations)
    stop = time.perf_counter()

    print(f'simulation time: {stop - start}')
    my_plot += p9.scale_y_continuous(limits=(0, 3_000))
    my_plot.draw()
    plt.show()
