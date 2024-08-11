import random
from multiprocessing import Pool
#just a file where to experiments are run...

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




# def f(y):
#     print("hey")
#     return("hey", y)
# def g(y):
#     print("howw")
#     return("hey", y)


# with Pool(10) as pool:
#     pool.map(f, range(100))
#     pool.map(g, range(100))

# list = [1,2,3]
# appendList = [3,4,5]
# extendList = [3,4,5]
# list.append(appendList)
# list.extend(extendList)
# print(list)
# print()
# for x in range(1000000):
#     print(x, end="\r")
# print(x)
list = [[0, 0]]*15
for t, x in enumerate(list):
    print(t, x)
    list[t][0] += 1
list.pop()
list.insert(1, 1)
print(list)