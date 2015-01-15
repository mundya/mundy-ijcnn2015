"""Take Nengo Networks and determine the memory required for a given max number
of neurons per core.

TODO: Account for synaptic filtering...
"""

import nengo
import nengo.networks
from nengo.utils.builder import (remove_passthrough_nodes,
                                 objs_and_connections, full_transform)
import numpy as np


def get_weight_matrices_requirements(network):
    # The weight matrix requirements for a core are the N_a x N_b_c matrix for
    # each preceding connection.
    (objects, connections) = remove_passthrough_nodes(
        *objs_and_connections(network))

    # For each Ensemble each incoming connection matrix is N_pre x N
    mem_usage = 0
    for ens in [o for o in objects if isinstance(o, nengo.Ensemble)]:
        # Get all incoming connections and hence all unique Ensemble sources
        sources = set([c.pre for c in connections if c.post is ens and
                       isinstance(c.pre, nengo.Ensemble)])
        pre_neurons = sum(s.n_neurons for s in sources)
        mem_usage += pre_neurons * ens.n_neurons

    return mem_usage * 4. # (4 bytes per value)


def get_factored_weight_matrices_requirements(network):
    (objects, connections) = remove_passthrough_nodes(
        *objs_and_connections(network))

    # For each Ensemble each incoming connection matrix is N_pre x N big
    mem_usage = 0
    for ens in [o for o in objects if isinstance(o, nengo.Ensemble)]:
        out_conns = [c for c in connections if c.pre is ens and
                     isinstance(c.post, nengo.Ensemble)]

        # Outgoing cost is (n_neurons + 1) x out_d where out_d is the number of
        # non-zero rows in the transform matrix
        out_transforms = [full_transform(c, allow_scalars=False) for c in
                          out_conns]
        out_dims = sum(np.sum(np.any(np.abs(t) > 0., axis=1)) for t in
                       out_transforms)
        mem_usage += (ens.n_neurons + 1) * out_dims

        # Incoming cost is just n_neurons x d
        mem_usage += ens.n_neurons * ens.dimensions

    return mem_usage * 4. # (4 bytes per value)
