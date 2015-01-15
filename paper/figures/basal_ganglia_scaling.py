if __name__ == '__main__':
    import analyse_weight_matrices as awm
    import nengo.networks
    import numpy as np
    import sys

    # Get the memory requirements for the basal ganglia in a variety of
    # configurations.  We know that the requirements scale with neurons for
    # weight matrices but scale with neurons AND dimensions for factored weight
    # matrices, so we'll test for both cases.
    n_neurons = [70]
    n_dimensions = [16, 32, 64, 128]  #, 256, 512]

    print("# Basal Ganglia Scaling")
    sys.stdout.write("# n_neurons ")
    for d in n_dimensions:
        sys.stdout.write("| WM%12dD |FWM%12dD " % (d, d))


    for n in n_neurons:
        sys.stdout.write("\n  %9d" % n)

        for d in n_dimensions:
            for f in [awm.get_weight_matrices_requirements,
                      awm.get_factored_weight_matrices_requirements]:
                net = nengo.networks.BasalGanglia(dimensions=d,
                                                  n_neurons_per_ensemble=n)
                mem = f(net) / 1024.  # Get the memory usage in kB
                sys.stdout.write(" %17.3f" % mem)
                sys.stdout.flush()

    print("")
