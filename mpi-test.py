from mpi4py import MPI

communicator = MPI.COMM_WORLD

print(f"Hello, I am {communicator.rank} of {communicator.size}.")
