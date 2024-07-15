import random
from multiprocessing import Pool


# for x in range(100):
#    print(random.random())

# line = [1,2,3,4,5]
# line2 = []
# for x in range(5):
#     line2.append(line.copy())

# line3 = []
# for x in line2:
#     line3.append(x.copy())

# line3[2][2] = 5

# print(line2[2][2])


#just a file where to experiments are run...

def f(y):
    print("hey")
    return("hey", y)
def g(y):
    print("howw")
    return("hey", y)


with Pool(10) as pool:
    pool.map(f, range(100))
    pool.map(g, range(100))