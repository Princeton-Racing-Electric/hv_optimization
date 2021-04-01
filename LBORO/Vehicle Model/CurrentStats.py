import matplotlib.pyplot as plt

def max_current(currents):
    return max(currents)

def average_current(currents):
    return sum(currents) / len(currents)

def peak_sustained_current(currents):
    peak_currents = []
    for i in range(5, len(currents)):
        subarray = currents[i-5:i+1]
        peak_currents.append(sum(subarray)/5)

    return max(peak_currents)

def plot_graphs(x, currents):
    plt.figure(1)
    plt.plot(x, currents)

    x = x[5:]

    peak_currents = []
    for i in range(5, len(currents)):
        subarray = currents[i - 5:i + 1]
        peak_currents.append(sum(subarray) / 5)

    plt.figure(2)
    plt.plot(x, peak_currents)
    plt.show()


# x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# c = [5, 6, 3, 6, 8, 2, 4, 0, 3, 2]
#
# print(x[5:])
# print(max_current(c))
# print(average_current(c))
# print(peak_sustained_current(c))
# plot_graphs(x, c)