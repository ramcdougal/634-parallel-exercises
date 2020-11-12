import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
import plotnine as p9
import time

# initial conditions
y = [0] * 1000
y[480:520] = [1] * 40

# time-step
dt = 0.01

# our rule for reaction-diffusion
def advance(dt, y):
    n = len(y)
    new_y = list(y)
    for j in range(n):
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
    start = time.perf_counter()

    # advance through t=100, plot
    # every 20
    for i in tqdm(range(int(100 / dt))):
        t = i * dt
        if t % 20 == 0:
            my_plot += plot_it(t, y)
        y = advance(dt, y)

    stop = time.perf_counter()
    print(f"elapsed time: {stop - start} s")

    my_plot.draw()
    plt.show()
