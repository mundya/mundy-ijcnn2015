import collections
import numpy
import pylab
import plot_settings
import seaborn as sns

# Times from reference simulator
reference = [
    ("build", [ 3.38, 6.8 ]),
    ("simulate", [ 65.3, 128.8 ])
]

# Times from nengo spinnaker
spinnaker = [
    ("build", [ 2.0, 4.7 ]),
    ("pacman", [ 9.6 - 5.0, 15.3 - 5.0 ]),
    ("load", [ 3.7, 10.1 ]),
    ("simulate", [ 14.5, 16.6 ]),
    ("download", [ 3.15, 5.3 ])
]

# Create single-axis figure
figure, axis = pylab.subplots(figsize=(plot_settings.column_width, 3), frameon=False)

bar_width = 0.5
bar_x = numpy.arange(2) * 1.5

# Colour strings
colours = {
    "build" : "0.1666",
    "pacman" : "0.3333",
    "load" : "0.5",
    "simulate" : "0.666",
    "download" : "0.833"
}

# Full labels
labels = {
    "build" : "Generation of network",
    "pacman" : "Generation of SpiNNaker data",
    "load" : "Uploading onto SpiNNaker",
    "simulate" : "Simulation",
    "download" : "Downloading from SpiNNaker"
}

# Draw an array of name, time tuples as a load of stacked bars
def stack(data, offset, legend):
    # Loop through stack
    bottom = numpy.zeros(2)
    for (key, times) in data:
        axis.bar(bar_x + offset, times, bottom=bottom, width=bar_width, label=labels[key] if legend else "_", color=colours[key])
        bottom += times

# Draw stacked bars
stack(reference, 0.0, False)
stack(spinnaker, bar_width, True)

axis.set_ylabel("Time / seconds")

axis.set_xticks(bar_x + bar_width)
axis.set_xticklabels(["16 dimensions, 8 actions", "32 dimensions, 16 actions"])

axis.legend(loc="upper left")

# Save figure
figure.tight_layout(pad=0.0)
figure.savefig("spa_wall_clock.pdf")
   
pylab.show()
