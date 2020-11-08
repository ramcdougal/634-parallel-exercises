import matplotlib.pyplot as plt
import multiprocessing
import sys
import numpy
import time

xlo = -2.5
ylo = -1.5
yhi = 1.5
xhi = 0.75
nx = 2048
ny = 1536
dx = (xhi - xlo) / nx
dy = (yhi - ylo) / ny

iter_limit = 200
set_threshold = 2

try:
	NUM_PROCESSES = int(sys.argv[1])
except:
	print(f"Run via: python {sys.argv[0]} NUM_PROCESSES")
	sys.exit(-1)


def mandelbrot_test(x, y):
	z = 0
	c = x + y * 1j
	for i in range(iter_limit):
		z = z ** 2 + c
		if abs(z) > set_threshold:
			return i
	return i


def calculate_line(y):
	return [mandelbrot_test(j * dx + xlo, y) for j in range(nx)]

def calculate_set():
	result = numpy.zeros([ny, nx])
	with multiprocessing.Pool(NUM_PROCESSES) as pool:
		lines = pool.map(calculate_line, [i * dy + ylo for i in range(ny)])
	for i, line in enumerate(lines):
		result[i, :] = line
	return result

if __name__ == '__main__':
	start_time = time.perf_counter()
	mandelbrot_set = calculate_set()
	stop_time = time.perf_counter()
	print(f'Calculation took {stop_time - start_time} seconds')
	plt.imshow(mandelbrot_set, interpolation='nearest', cmap='Greys')
	plt.gca().set_aspect('equal')
	plt.axis('off')
	plt.show()
