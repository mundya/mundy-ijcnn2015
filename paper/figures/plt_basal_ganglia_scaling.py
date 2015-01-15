import numpy as np

if __name__ == '__main__':
    # Read in the data
    data = np.genfromtxt('basal_ganglia_scale.dat')
    if len(data.shape) == 1:
        data.shape = (1,) + data.shape

    # For each row create a new scaling cost table
    for d in data:
        # Get the number of neurons per dimension
        neurons_per_dimension = int(d[0])
        full_weight_matrix = d[1::2]
        factored_weight_matrix = d[2::2]

        # Get the dimensionalities
        assert len(full_weight_matrix) == len(factored_weight_matrix)
        dims = [1<<(4+n) for n in range(len(factored_weight_matrix))]

        # Determine the memory reduction
        reduction = ((full_weight_matrix - factored_weight_matrix) /
                     full_weight_matrix)

        # Print the table
        with open("bgscale_{:d}.tex".format(neurons_per_dimension), "w+") as f:
            # The header
            f.write("""
\\begin{tabular}{r %s}
  \\toprule
    Dimensionality & %s \\\\
  \\midrule\n""" % (
                        ' '.join(['S'] * len(dims)),
                        ' & '.join(['{' + str(n) + '}' for n in dims])
                    )
            )

            # The full weight matrix size
            f.write("    Full weight matrix / \\si{\\mebi\\byte}")
            for v in full_weight_matrix:
                f.write(" & {:.2f}".format(v / 1024.0))
            f.write("\\\\\n")

            # The factored weight matrix size
            f.write("    Factored / \\si{\\mebi\\byte}")
            for v in factored_weight_matrix:
                f.write(" & {:.2f}".format(v / 1024.))
            f.write("\\\\\n")

            # The reduction
            f.write("    Reduction / \\si{\\percent}")
            for v in reduction:
                f.write(" & {:.2f}".format(v * 100))
            f.write("\\\\\n")

            f.write("  \\bottomrule\n\\end{tabular}\n")
