import collections
import numpy
import pylab
import plot_settings
import seaborn as sns

# Times from reference simulator
reference = [
    ("build", [ 3.82, 6.66 ]),
    ("simulate", [ 70, 133.69 ])
]

# Times from nengo spinnaker
# **NOTE** 5s is boot time
spinnaker = [
    ("build", [ 2.53 + (10.54 - 5.0), 4.39 + (14.70 - 5.0)]),
    ("load", [ 3.94, 4.37 ]),
    ("simulate", [ 14.40, 16.42 ]),
    ("download", [ 1.54, 3.12 ])
]

# Create single-axis figure
figure, axis = pylab.subplots(figsize=(plot_settings.column_width, 3), frameon=False)

bar_pad = 0.1
bar_width = 0.5
bar_spacing = 0.05
bar_x = bar_pad + numpy.arange(2) * 1.5

# Colour strings
cmap = sns.color_palette("colorblind")
hatches = {
    "build" : { "color" : "0.5" }, 
    "load" :  { "hatch" : "||", "color" : "white" },
    "simulate" : { "color" : "0.75" },
    "download" : { "hatch" : "||||", "color" : "white" } 
}

# Full labels
labels = {
    "build" : "Generation",
    "load" : "Uploading",
    "simulate" : "Simulation",
    "download" : "Downloading"
}

# Draw an array of name, time tuples as a load of stacked bars
def stack(data, offset, legend):
    # Loop through stack
    bottom = numpy.zeros(2)
    for (key, times) in data:
        axis.bar(bar_x + offset, times, bottom=bottom, label=labels[key] if legend else "_",
                 width=bar_width, **hatches[key])
        bottom += times

def get_total(data, experiment_index):
    time = 0.0
    for (key, times) in data:
        time += times[experiment_index]
    
    return time

# Draw stacked bars
stack(reference, 0.0, False)
stack(spinnaker, bar_width + bar_spacing, True)

axis.set_ylabel("Time / s")
    
# Combine bar positions to get tick positions
ticks = numpy.concatenate((bar_x, bar_x + bar_width + bar_spacing))
ticks = numpy.sort(ticks + (bar_width / 2.0))
axis.set_xticks(ticks)
axis.set_xticklabels(["Nengo", "SpiNNaker", "Nengo", "SpiNNaker"], size="xx-small")

axis.text(bar_x[0] + bar_width, -27.0, "8 actions", horizontalalignment="center", size="small")
axis.text(bar_x[1] + bar_width, -27.0, "16 actions", horizontalalignment="center", size="small")

handles, labels = axis.get_legend_handles_labels()
axis.legend(handles[::-1], labels[::-1], loc="upper left")

# Save figure
figure.tight_layout(pad=0.0)

# Faff with box after layout
box = axis.get_position()
axis.set_position([box.x0, 0.2, box.width, 0.7])

figure.savefig("spa_wall_clock.pdf")

# Calculate speedup
for t in range(2):
    print "Experiment %u: Speedup: %f" % (t, get_total(reference, t) / get_total(spinnaker, t))


pylab.show()
