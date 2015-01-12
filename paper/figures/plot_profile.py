import collections
import csv
import numpy
import pylab
import plot_settings
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
import seaborn as sns

def load_results(csv_filename):
    with open(csv_filename, "rb") as csv_file:
        return list(csv.reader(csv_file))

def plot_contour(results, get_x_function, get_y_function, filter_function, title, x_label, y_label, filename, include_output):
     # Create single-axis figure
    figure, axis = pylab.subplots(figsize=(plot_settings.column_width, 3), frameon=False)
    
    # Generate x, y, z data
    if include_output:
        filtered_results = [[get_x_function(r), get_y_function(r), float(r[6])] for r in results if filter_function(r)]
    else:
        filtered_results = [[get_x_function(r), get_y_function(r), float(r[6]) - float(r[9])] for r in results if filter_function(r)]
    
    # Sort tuples and unzip into stackplot friendly form
    filtered_results.sort()
    unzipped_results = zip(*filtered_results)
    
    xi = numpy.linspace(min(unzipped_results[0]), max(unzipped_results[0]))
    yi = numpy.linspace(min(unzipped_results[1]), max(unzipped_results[1]))
    
    zi = griddata((unzipped_results[0], unzipped_results[1]), unzipped_results[2], (xi[None,:], yi[:,None]), method='cubic')
   
    contours = axis.contour(xi, yi, zi, cmap=sns.dark_palette('gray', as_cmap=True, n_colors=4, reverse=True), levels=[0.2, 0.4, 0.6, 0.8])
    manual = [(8.0, 175), (2.5, 740), (4.0, 960), (6, 1140)]
    axis.clabel(contours, fmt=lambda n: '{:.0f}%'.format(n*100), manual=manual)

    if title is not None:
        axis.set_title(title)
    axis.set_xlabel(x_label)
    axis.set_ylabel(y_label)
    
    # Use log2 scale for dimensions
    axis.set_xscale('log', basex=2)
   
    # Use dimensions of data points for x ticks
    axis.set_xticks(unzipped_results[0])
    axis.set_xticklabels(unzipped_results[0])

    axis.set_yticks([0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000])
    
    # Save figure
    figure.tight_layout(pad=0.0)
    figure.savefig(filename)
     
def plot_surface(results, get_x_function, get_y_function, filter_function, title, x_label, y_label, filename):
    # Create 3D figure
    figure = pylab.figure(figsize=(plot_settings.column_width, 3.5), frameon=False)
    axis = figure.add_subplot(111, projection="3d")
    
    # Generate x, y, z data
    filtered_results = [[get_x_function(r), get_y_function(r), float(r[6])] for r in results if filter_function(r)]

    # Sort tuples and unzip into stackplot friendly form
    filtered_results.sort()
    unzipped_results = zip(*filtered_results)
    
    # Plot triangle-surface
    axis.plot_trisurf(unzipped_results[0], unzipped_results[1], unzipped_results[2], cmap = pylab.cm.coolwarm, shade = True)
    
    if title is not None:
        axis.set_title(title)
    axis.set_xlabel(x_label)
    axis.set_ylabel(y_label)
    axis.set_zlabel("CPU load")
    
    # Save figure
    figure.tight_layout(pad=0.5)
    figure.savefig(filename)
    
def plot_stack(results, get_x_function, filter_function, title, x_label, filename):
    # Create single-axis figure
    figure, axis = pylab.subplots(figsize=(plot_settings.column_width, 3.5), frameon=False)
    
    # Filter results
    filtered_results = [[get_x_function(r), float(r[7]), float(r[8]), float(r[9])] for r in results if filter_function(r)]
    
    # Sort tuples and unzip into stackplot friendly form
    filtered_results.sort()
    unzipped_results = zip(*filtered_results)

    # Show on stackplot
    stackPlotPolys = axis.stackplot(unzipped_results[0], unzipped_results[1:])
    
    # **HACK** add proxies objects with same face colour as stack plot polygons so they can be added to legend
    legendProxies = []
    for poly in stackPlotPolys:
        legendProxies.append(pylab.Rectangle((0, 0), 1, 1, fc=poly.get_facecolor()[0]))
        
    # Add legend
    figure.legend(legendProxies, ["Input filtering", "Neuron update", "Output"])
    
    # Setup axis
    if title is not None:
        axis.set_title(title)
    axis.set_xlabel(x_label)
    axis.set_ylabel("CPU time")
    axis.set_xlim((min(unzipped_results[0]), max(unzipped_results[0])))
    axis.set_ylim((0.0, 1.0))
    
    # Save figure
    figure.tight_layout(pad=0.5)
    figure.savefig(filename)

def plot_stack_bar(results, get_x_function, filter_function, title, x_label, filename):
    # Create single-axis figure
    figure, axis = pylab.subplots(figsize=(plot_settings.column_width, 3), frameon=False)
    
    # Filter results
    filtered_results = [[get_x_function(r), float(r[7]) * 100.0, float(r[8]) * 100.0, float(r[9]) * 100.0] for r in results if filter_function(r)]
    
    # Sort tuples and unzip into stackplot friendly form
    filtered_results.sort()
    unzipped_results = zip(*filtered_results)

    bar_pad = 0.1
    bar_x = bar_pad + numpy.arange(len(unzipped_results[0]))
    bar_width = 0.5
    
    cmap = sns.color_palette("colorblind")
    axis.bar(bar_x, unzipped_results[1], label="Input filtering", color=cmap[0],
             width=bar_width, edgecolor="none")
    axis.bar(bar_x, unzipped_results[2], bottom=unzipped_results[1], label="Neuron update", color=cmap[1],
             width=bar_width, edgecolor="none")
    axis.bar(bar_x, unzipped_results[3], bottom=unzipped_results[2], label="Output", color=cmap[2],
             width=bar_width, edgecolor="none")
    
    if title is not None:
        axis.set_title(title)
    axis.set_xlabel(x_label)
    axis.set_ylabel("Simulation time step CPU time %")
    
    axis.set_xticks(bar_x + (bar_width / 2.))
    axis.set_xticklabels(unzipped_results[0])

    axis.legend(loc='upper left')
    
    # Save figure
    figure.tight_layout(pad=0.0)
    figure.savefig(filename)
    
# Load results CSV file
results = load_results("profile_paper.csv")

# Plot stuff
plot_stack_bar(results, 
    lambda r: int(r[1]),
    lambda r: int(r[0]) == 16 and int(r[2]) == 0,
    None,
    "Number of neurons",
    "comm_channel_cpu_16d_bar.pdf")
'''
plot_stack(results, 
    lambda r: int(r[0]),
    lambda r: int(r[1]) == 200 and int(r[2]) == 0,
    "CPU time when simulating 200 neuron ensembles with varying dimensionality",
    "Number of dimensions")

plot_stack(results, 
    lambda r: int(r[1]),
    lambda r: int(r[0]) == 16 and int(r[2]) == 0,
    "CPU time when simulating 16D ensembles of varying sizes",
    "Ensemble size")
'''
plot_contour(results,
    lambda r: int(r[0]),
    lambda r: int(r[1]),
    lambda r: int(r[2]) == 0,
    None,
    "Number of dimensions",
    "Number of neurons",
    "comm_channel_cpu_contour.pdf",
    True)

plot_contour(results,
    lambda r: int(r[0]),
    lambda r: int(r[1]),
    lambda r: int(r[2]) == 0,
    None,
    "Number of dimensions",
    "Number of neurons",
    "comm_channel_cpu_contour_no_output.pdf",
    False)

pylab.show()
