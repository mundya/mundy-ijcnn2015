import datetime
import math
import matplotlib.pyplot as plt
import nengo
import nengo.spa as spa
import numpy
from nengo.utils.distributions import Uniform

semantic_pointer_dimensions = 16
num_inputs = 16
input_presentation_time = 0.1
spinnaker = True

def profile(name, last):
    now = datetime.datetime.now()
    print "%s:%s (%s)" % (name, now, (now - last).total_seconds())
    return now

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
    
    #input_probe = nengo.Probe(state)
    #utility_probe = nengo.Probe(Q.output)
    
    bg = nengo.networks.BasalGanglia(num_inputs)
    nengo.Connection(Q.output, bg.input)
    
    #bg_probe = nengo.Probe(bg.output)
    
    R = nengo.networks.EnsembleArray(64, num_inputs, label='R',
        encoders=[[1]]*64, intercepts=Uniform(0.2, 1))
    nengo.Connection(bg.output, R.input)
    output_probe = nengo.Probe(R.output) 
    
    bias = nengo.Node([1], label='bias')
    nengo.Connection(bias, R.input, transform=numpy.ones((num_inputs, 1)), synapse=None)

    nengo.Connection(R.output, R.input, transform=(numpy.eye(num_inputs)-1), synapse=0.008)
    
    if not spinnaker:
        track = profile("Building", datetime.datetime.now())
        sim = nengo.Simulator(model)
        profile("Building done", track)
    else:
        import nengo_spinnaker

        config = nengo_spinnaker.Config()
        config[input_node].f_of_t = True

        sim = nengo_spinnaker.Simulator(model, config=config)
    
    track = profile("Running", datetime.datetime.now())
    sim.run(10.0)
    profile("Running done", track)
    
    #fig, axis = plt.subplots(4)
    fig, axis = plt.subplots()
    '''
    axis[0].plot(sim.trange(), spa.similarity(sim.data, input_probe))
    axis[0].legend(vocab_strings, fontsize='x-small')
    axis[0].set_ylabel('Input')
    
    axis[1].plot(sim.trange(), sim.data[utility_probe])
    axis[1].legend(vocab_strings, fontsize='x-small')
    axis[1].set_ylabel('Utility')
    
    axis[2].plot(sim.trange(), sim.data[bg_probe])
    axis[2].legend(vocab_strings, fontsize='x-small')
    axis[2].set_ylabel("Basal ganglia output")
    
    axis[3].plot(sim.trange(), sim.data[output_probe])
    axis[3].legend(vocab_strings, fontsize='x-small')
    axis[3].set_ylabel("Biased selection")
    '''
    axis.plot(sim.trange(), sim.data[output_probe])
    axis.legend(vocab_strings, fontsize='x-small')
    axis.set_ylabel("Biases Basal Ganglia Selection")
    plt.show()
