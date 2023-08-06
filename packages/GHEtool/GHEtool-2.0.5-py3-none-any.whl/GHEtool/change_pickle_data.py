import pickle
import numpy as np

from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir("Data/") if isfile(join("Data/", f))]

for name in onlyfiles:
    print(name)
    data = pickle.load(open("Data/" + name, 'rb'))
    # B, k_s

    for B in (3, 4, 5, 6, 7, 8, 9):
        for k_s in (1, 1.5, 2, 2.5, 3, 3.5, 4):
            temp = data[B].pop(k_s)
            data[B][k_s / (2.4 * 10 ** 6)] = temp

    pickle.dump(data, open("Data/" + name, "wb"))