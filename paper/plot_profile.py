import collections
import csv
import numpy
import pylab
import plot_settings
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

def load_results(csv_filename):
    with open(csv_filename, "rb") as csv_file:
        return list(csv.reader(csv_file))

def plot_contour(results, get_x_function, get_y_function, filter_function, title, x_label, y_label):
     # Create single-axis figure
    figure, axis = pylab.subplots()
    
    # Generate x, y, z data
    filtered_results = [[get_x_function(r), get_y_function(r), float(r[6])] for r in results if filter_function(r)]
    
    # Sort tuples and unzip into stackplot friendly form
    filtered_results.sort()
    unzipped_results = zip(*filtered_results)
    
    xi = numpy.linspace(min(unzipped_results[0]), max(unzipped_results[0]))
    yi = numpy.linspace(min(unzipped_results[1]), max(unzipped_results[1]))
    zi = griddata((unzipped_results[0], unzipped_results[1]), unzipped_results[2], (xi[None,:], yi[:,None]), method='cubic')
   
    contours = axis.contour(xi, yi, zi, cmap=pylab.cm.gray, levels=[0.2, 0.4, 0.6, 0.8])
    axis.clabel(contours)

    axis.set_title(title)
    axis.set_xlabel(x_label)
    axis.set_ylabel(y_label)
    
    # Use log2 scale for dimensions
    axis.set_xscale('log', basex=2)
   
    # Use dimensions of data points for x ticks
    axis.set_xticks(unzipped_results[0])
    axis.set_xticklabels(unzipped_results[0])
     
def plot_surface(results, get_x_function, get_y_function, filter_function, title, x_label, y_label):
    # Create 3D figure
    figure = pylab.figure()
    axis = figure.add_subplot(111, projection="3d")
    
    # Generate x, y, z data
    filtered_results = [[get_x_function(r), get_y_function(r), float(r[6])] for r in results if filter_function(r)]

    # Sort tuples and unzip into stackplot friendly form
    filtered_results.sort()
    unzipped_results = zip(*filtered_results)
    
    # Plot triangle-surface
    axis.plot_trisurf(unzipped_results[0], unzipped_results[1], unzipped_results[2], cmap = pylab.cm.coolwarm, shade = True)
    
    axis.set_title(title)
    axis.set_xlabel(x_label)
    axis.set_ylabel(y_label)
    axis.set_zlabel("CPU load")
    
def plot_stack(results, get_x_function, filter_function, title, x_label):
    # Create single-axis figure
    figure, axis = pylab.subplots()
    
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
    axis.set_title(title)
    axis.set_xlabel(x_label)
    axis.set_ylabel("CPU time")
    axis.set_xlim((min(unzipped_results[0]), max(unzipped_results[0])))
    axis.set_ylim((0.0, 1.0))

def plot_stack_bar(results, get_x_function, filter_function, title, x_label):
    # Create single-axis figure
    figure, axis = pylab.subplots()
    
    # Filter results
    filtered_results = [[get_x_function(r), float(r[7]) * 100.0, float(r[8]) * 100.0, float(r[9]) * 100.0] for r in results if filter_function(r)]
    
    # Sort tuples and unzip into stackplot friendly form
    filtered_results.sort()
    unzipped_results = zip(*filtered_results)

    bar_x = numpy.arange(len(unzipped_results[0]))
    bar_width = 0.5
    
    axis.bar(bar_x, unzipped_results[1], width=bar_width, label="Input filtering", color="0.25")
    axis.bar(bar_x, unzipped_results[2], bottom=unzipped_results[1], width=bar_width, label="Neuron update", color="0.5")
    axis.bar(bar_x, unzipped_results[3], bottom=unzipped_results[2], width=bar_width, label="Output", color="0.75")
    
    axis.set_title(title)
    axis.set_xlabel(x_label)
    axis.set_ylabel("Simulation time step CPU time %")
    
    axis.set_xticks(bar_x + (bar_width / 2.))
    axis.set_xticklabels(unzipped_results[0])

    axis.legend()
    
# Load results CSV file
results = load_results("profile_paper.csv")

# Plot stuff
plot_stack_bar(results, 
    lambda r: int(r[1]),
    lambda r: int(r[0]) == 16 and int(r[2]) == 0,
    "CPU time when simulating 16D ensembles of varying sizes",
    "Ensemble size")
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
    "CPU time when simulating neuron ensembles with varying dimensionality and size",
    "Number of dimensions",
    "Ensemble size")

pylab.show()
