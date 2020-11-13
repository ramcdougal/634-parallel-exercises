# 634-parallel-exercises

## Notes

Strictly speaking, the Mandelbrot set is the set of points that never diverge in the iteration, however it is common to color/shade graphs by how quickly the point diverges, as is done here.

For this lab, when going from 1 to 2 processes, we won't get identical results from stochastic_diffusion. How can we tell if we did it right then?

On my machine, the MPI benefits for propagating-signal-mpi.py really only exist for going from 1 to 2 processes... after that, there's no speedup, presumably because the compute time per process is small.
