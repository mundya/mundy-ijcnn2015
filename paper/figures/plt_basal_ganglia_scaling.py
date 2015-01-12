import numpy as np
from matplotlib import pyplot as plt

try:
    import seaborn as sns
    sns.set(context='paper', style='whitegrid')
except ImportError:
    print "No seaborn :("
    pass

if __name__ == '__main__':
    # Read in the data
    data = np.genfromtxt('basal_ganglia_scale.dat').T

    # Plot each of the dimensions
    f, axs = plt.subplots(1, 2, figsize=(8, 3.5), sharex=True)

    for i, d in enumerate([16, 32, 64, 128]):
        axs[0].plot(data[0], data[1 + i*2] / 1024., label="%d dimensions" % d)
        axs[1].plot(data[0], data[1 + i*2 + 1] / 1024.)

    axs[1].set_xlabel("Number of neurons per Ensemble")

    axs[0].set_ylabel("Total memory utilisation / MB")
    axs[1].set_ylabel("Total memory utilisation / MB")

    axs[0].set_title("Weight Matrices")
    axs[1].set_title("Factored Weight Matrices")

    axs[0].legend(loc=2)
    axs[1].legend(loc=2)

    plt.tight_layout(h_pad=3)

    f.savefig('basal_ganglia_scaling.png')

    # Generate a table of reductions
    rdat = list()
    for d in data.T:
        dat = list()
        dat.append(d[0])

        for n in range(4):
            dat.append((d[1+n*2] - d[2+n*2]) / d[1+n*2])

        rdat.append(dat)

    np.savetxt('bg_reductions.csv', rdat)
