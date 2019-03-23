import timeit
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def timed_run(function, count, length, min_sequence_length, max_sequence_length) -> float:
    return timeit.timeit(
        stmt="{}(input_list=input_list, min_sequence_length={}, max_sequence_length={})"
            .format(function, min_sequence_length, max_sequence_length),
        setup="""
from random_list import random_list
from {} import {}
input_list = random_list(count={}, length={})
    """.format(function, function, count, length), number=1)


times = np.zeros((11, 11), float)
for i in range(1, 11):
    for j in range(1, 11):
        count = i
        length = j*100
        print("count: {}, length: {}".format(count, length))
        times[i, j] = timed_run(
            function="iterate_and_count",
            count=count,
            length=length,
            min_sequence_length=2,
            max_sequence_length=length)

print(times)

hf = plt.figure()
ha = hf.add_subplot(111, projection='3d')

X, Y = np.meshgrid(range(11), range(11))  # `plot_surface` expects `x` and `y` data to be 2D
ha.plot_surface(X, Y, times)

plt.show()
