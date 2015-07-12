"""Construct a demonstration of the NEF in action.
"""

import numpy as np
import nengo
from matplotlib import pyplot as plt
import plot_settings

# Create the Nengo model and simulate
with nengo.Network("Sample network") as network:
    # Create the Ensemble to simulate
    ens = nengo.Ensemble(4, 2)

    # Set the encoders to be 90-degree spaced around a circle at a 45-degree
    # initial offset.
    angles = (np.array([0, 0.5, 1.0, 1.5]) + 0.25)*np.pi
    ens.encoders = np.vstack([np.sin(angles), np.cos(angles)]).T

    # Set the max rates at something low so as to be visible.
    ens.max_rates = np.random.uniform(5., 20., size=ens.n_neurons)

    # Set the intercepts
    ens.intercepts = np.array([-.25]*ens.n_neurons)

    # Create the sine/cosine source
    inp = nengo.Node(lambda t: [np.sin(t), np.cos(t)])

    # Create probes for (1) input, (2) decoded output and (3) spikes
    p_inp = nengo.Probe(inp, synapse=0.0)
    p_out = nengo.Probe(ens, synapse=0.5)
    p_spikes = nengo.Probe(ens.neurons)

    # Connect the input to the ensemble
    nengo.Connection(inp, ens)

# Simulate for one full rotation
sim = nengo.Simulator(network)
sim.run(2*np.pi*1.)

# Plot (figsize determined from column width)
from nengo.utils.matplotlib import rasterplot
from nengo.utils.ensemble import response_curves
fig = plt.figure(figsize=(8, 6.5), frameon=False)

# Input and spikes
ax0 = fig.add_subplot(211)
ax0.plot(sim.trange(), sim.data[p_inp])
ax0.set_ylabel('Input')
ax0.set_xlabel('Time / s')

ax1 = ax0.twinx()
rasterplot(sim.trange(), sim.data[p_spikes], ax1)
ax1.set_yticks([])
ax1.set_title('Neuronal responses')

# Tuning curves
ax2 = fig.add_subplot(223)

for n, a in enumerate(['a', 'b', 'c', 'd']):
    angles = np.linspace(0, 2*np.pi, 100)
    vecs = np.vstack([np.sin(angles), np.cos(angles)]).T
    encoded = []

    for v in vecs[:]:
        encoded.append(np.dot(ens.encoders[n], v))

    ins, response = response_curves(ens, sim, np.array(encoded))
    assert np.all(ins == encoded)
    ax2.plot(angles, response.T[n])

ax2.set_xlim(0, 2*np.pi)
ax2.set_xlabel("Angle")
ax2.set_xticks(np.array([0, 0.5, 1.0, 1.5, 2.0]) * np.pi)
ax2.set_xticklabels(['$0$', '$0.5\pi$', '$\pi$', '$1.5\pi$', '$2\pi$'])
ax2.set_ylabel("Firing rate / Hz")
ax2.set_title('Tuning curves')

# Output and direction vectors
ax3 = fig.add_subplot(224)
ax3.set_aspect(1)
xs, ys = sim.data[p_out].T
n_points = len(xs) - 1

for n in range(n_points):
    ax3.plot(xs[n:n+2], ys[n:n+2],
             linewidth=1,
             color='{:f}'.format((1. - float(n)/n_points) * .5))

xs, ys = sim.data[p_inp].T
n_points = len(xs) - 1

for n in range(n_points):
    ax3.plot(xs[n:n+2], ys[n:n+2],
             linewidth=1,
             color='{:f}'.format((1. - float(n)/n_points) * .5))

ax3.set_xlim([-1, 1])
ax3.set_ylim([-1, 1])
ax3.set_title('Decoded output')

fig.tight_layout(pad=0.5)
fig.savefig('nef-1.pdf')
