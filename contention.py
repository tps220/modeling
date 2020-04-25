import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import numpy
import random

numBuckets = 40
buckets = []
for iterator in range(0, numBuckets):
    buckets.append([])

height = []
x = []
for i in range(0, numBuckets):
    height.append(0)
    x.append(i)

numThreads = 64
threads = []
for iterator in range(0, numThreads):
    threads.append(int(random.random() * 100000))

def holding():
    nextIteration = []
    for i in range(0, len(buckets)):
        if len(buckets[i]) > 0:
            element = buckets[i].pop(0)
            nextIteration.append(element)
    for thread in nextIteration:
        index = int(random.random() * numBuckets)
        buckets[index].append(thread)

    for i in range(0, len(buckets)):
        height[i] = len(buckets[i])
    return height

def update_hist(d):
    new_heights = holding()
    plt.plot(x, new_heights)

def play_n_rounds(n):
    data = []
    for iterator in range(0, n):
        new_heights = holding()
        data.append(new_heights.copy())

    avg_mean = 0
    avg_variance = 0
    for round in data:
        instances = 0
        dev = 0
        for i in round:
            if i > 0:
                instances = instances + 1
        mean = numThreads / instances
        for i in round:
            if i > 0:
                dev += pow(mean - i, 2)
        dev /= instances
        dev = pow(dev, 0.5)

        avg_mean += mean
        avg_variance += dev

    avg_variance /= len(data)
    avg_mean /= len(data)
    return (avg_mean, avg_variance)

def zero_round():
    for i in range(0, numThreads):
        index = int(random.random() * numBuckets)
        buckets[index].append(threads[i])
    for i in range(0, len(buckets)):
        height[i] = len(buckets[i])


zero_round()
ts = [1, 4, 8, 16, 32, 48, 64, 80, 96, 112, 128, 140, 180]
bs = numpy.arange(16, 100000, 32)
data = []
for t in ts:
    results = []
    numThreads = t
    threads = []
    for iterator in range(0, numThreads):
        threads.append(int(random.random() * 100000))
    for b in bs:
        if len(data) > 0 and data[len(data) - 1] > b:
            continue
        numBuckets = b
        buckets = []
        for iterator in range(0, numBuckets):
            buckets.append([])

        height = []
        x = []
        for i in range(0, numBuckets):
            height.append(0)
            x.append(i)

        zero_round()
        (avg_mean, avg_variance) = play_n_rounds(100)
        print(str(b) + ", " + str(avg_mean))
        if (avg_mean < 1.05):
            print(avg_mean)
            print(t)
            print(b)
            data.append(b)
            break
        #results.append(avg_mean)
        #results.append([avg_mean, avg_variance])


fig = plt.figure()
p0 = plt.plot(ts, data)
plt.show()

#zero_round()
#fig = plt.figure()
#hist = plt.bar(x, height)

#animation = animation.FuncAnimation(fig, update_hist, 1)
#plt.show()