import csv
import numpy
from matplotlib import cm
from matplotlib import pyplot
import plot_settings

def plot_contours(dimensions, ensemble_sizes, cpu_matrix):
    # Plot contours
    fig, axis = pyplot.subplots(figsize=(6,4))
    contours = axis.contour(dimensions, ensemble_sizes, cpu_matrix.T, cmap=cm.coolwarm, levels = [0, 0.25, 0.5, 0.75, 1.0])
    pyplot.clabel(contours)
    
 
    axis.set_xlabel("Number of dimensions")
    axis.set_ylabel("Number of neurons per ensemble")
    
    # Use log2 scale for dimensions
    axis.set_xscale('log', basex=2)
   
    # Use dimensions of data points for x ticks
    axis.set_xticks(dimensions)
    axis.set_xticklabels(dimensions)
    
with open("profile_paper.csv", "rb") as csvfile:
    csvreader = csv.reader(csvfile)
    
    dimensions = [1, 2, 4, 8, 16, 32, 64]
    ensemble_sizes = [10, 20, 50, 100, 200, 500, 1000, 2000]
    cpu_matrix = numpy.ones((len(dimensions), len(ensemble_sizes))) * 1000.0
     
    # Read all rows
    for row in csvreader:
        # Find index of dimension and ensemble size in cpu matrix
        d = dimensions.index(int(row[0]))
        e = ensemble_sizes.index(int(row[1]))
        
        # Add total cpu load to matrix
        cpu_matrix[d][e] = float(row[6])
    
    numpy.set_printoptions(linewidth=250)
    print cpu_matrix
    #print cpu_matrix
    
    plot_contours(dimensions, ensemble_sizes, cpu_matrix)
    
    pyplot.show()