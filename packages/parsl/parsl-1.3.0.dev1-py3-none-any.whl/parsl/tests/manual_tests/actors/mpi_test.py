from mpi4py import MPI
import time
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

n = 1000000

if rank == 0:
    x = 0
    t = time.time()
    for i in range(n):
        comm.send(i, dest=1, tag=11)
    delta = time.time() - t
    print("Sum : ", x)
    print("Done in {:8.3f} Msgs/s".format(n / delta))

elif rank == 1:

    for i in range(n):
        data = comm.recv(source=0, tag=11)
