from matplotlib import pyplot
import time
try:
	from randomstate.prng.pcg64 import RandomState
except ImportError:
	print """Importing randomstate failed. To fix, try:
	pip install randomstate"""
	import sys
	sys.exit()

random_seed = 1
random_stream = 1
prng = RandomState(random_seed, random_stream)

x_lo = 0
x_hi = 200
num_molecules = 10000
molecule_locations = [100] * num_molecules

# our rule for diffusion
def advance(molecules):
	for i, mol_loc in enumerate(molecules):
		r = prng.uniform()
		if r < 0.4:
			molecules[i] = max(x_lo, mol_loc - 1)
		elif r < 0.8:
			molecules[i] = min(x_hi, mol_loc + 1)

def plot_it(molecules, label=''):
	counts = [0] * (x_hi - x_lo + 1)
	for mol_loc in molecules:
		counts[mol_loc] += 1
	pyplot.plot(counts, label=label)

if __name__ == '__main__':
	start = time.time()
	for t in range(2001):
		if t % 400 == 0:
			plot_it(molecule_locations, 't = %g' % t)
		advance(molecule_locations)
	stop = time.time()

	print 'simulation time:', stop - start

	pyplot.legend()
	pyplot.ylim([0, 300])
	pyplot.show()