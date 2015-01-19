import math
import matplotlib.pyplot as plt
import nengo
import nengo.spa as spa
import nengo_spinnaker
import numpy
import plot_settings
import seaborn as sns
from nengo.utils.distributions import Uniform

semantic_pointer_dimensions = 16
num_inputs = 4
input_presentation_time = 0.1

def num_to_string(num, length):
    string = ""
    for i in range(length):
        divider = 26 ** i
        string += chr(ord("A") + (num / divider) % 26)
    
    return string

def build_vocab(num, length):
    return [vocab.parse(num_to_string(i, length)).v for i in range(num)]

model = nengo.Network()

with model:
    vocab = spa.Vocabulary(semantic_pointer_dimensions)   
    
    # Build ensemble to represent input semantic pointer
    state = nengo.Ensemble(64 * semantic_pointer_dimensions, semantic_pointer_dimensions, label='state')
    
    # Build ensemble array with 64 neurons per dimension to represent Q values
    Q = nengo.networks.EnsembleArray(64, num_inputs, label='Q')

    vocab_strings = [num_to_string(i, 1) for i in range(num_inputs)]
    vocab_transform = [vocab.parse(s).v for s in vocab_strings]
    
    # Create node to provide sequence of vocab semantic pointers
    input_node = nengo.Node(
        lambda t: vocab_transform[int(math.floor(t / input_presentation_time)) % num_inputs])
    
    # Transform state in semantic pointer to Q values based on similarity with vocab
    state.vocab = vocab
    nengo.Connection(state, Q.input, transform=vocab_transform)
    
    nengo.Connection(input_node, state)
    
    q_probe = nengo.Probe(Q.output, synapse=0.01)
    
    bg = nengo.networks.BasalGanglia(num_inputs)
    nengo.Connection(Q.output, bg.input)
    
    R = nengo.networks.EnsembleArray(64, num_inputs, label='R',
        encoders=[[1]]*64, intercepts=Uniform(0.2, 1))
    nengo.Connection(bg.output, R.input)
    output_probe = nengo.Probe(R.output, synapse=0.01) 
    
    bias = nengo.Node([1], label='bias')
    nengo.Connection(bias, R.input, transform=numpy.ones((num_inputs, 1)), synapse=None)

    nengo.Connection(R.output, R.input, transform=(numpy.eye(num_inputs)-1), synapse=0.008)
    
    config = nengo_spinnaker.Config()
    config[input_node].f_of_t = True

    sim = nengo_spinnaker.Simulator(model, config=config)
    
    sim.run(0.5)
    
    fig, axis = plt.subplots(2, sharex=True, figsize=(plot_settings.column_width, 3.5), frameon=False)

    axis[0].plot(sim.trange(), sim.data[q_probe])
    axis[0].set_ylabel("Input utility")
    
    lines = axis[1].plot(sim.trange(), sim.data[output_probe])
    axis[1].set_xlabel("Time / s")
    axis[1].set_ylabel("Basal ganglia output")
    
    
    fig.legend(lines, vocab_strings, fontsize='x-small', ncol=4, loc="upper center")
    plt.show()
    
    # Save figure
    fig.tight_layout(pad=0.0)
    fig.savefig("basal_ganglia.pdf")