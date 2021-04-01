from matplotlib import pyplot as plt

def plotter(x_arr, y_arr):

    plt.plot(x_arr, y_arr)
    plt.savefig('Fig.png')