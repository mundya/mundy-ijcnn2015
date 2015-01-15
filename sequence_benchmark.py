import datetime
import nengo
import nengo.spa as spa

spinnaker = False

dimensions = 16

def profile(name, last):
    now = datetime.datetime.now()
    print "%s:%s (%s)" % (name, now, (now - last).total_seconds())
    return now

class Sequence(spa.SPA):
    def __init__(self, num_actions):
        spa.SPA.__init__(self)
        
        #Specify the modules to be used
        self.cortex = spa.Buffer(dimensions=dimensions)
        
        # Generate names for actions
        def int_to_ascii(i):
            return chr(ord("A") + i)
        
        # Generate sequential action names
        self.action_names = [int_to_ascii((i / 26) % 26) + int_to_ascii(i % 26) for i in range(num_actions)]
      
        # From this build action mapping
        action_mappings = ["dot(cortex, %s) --> cortex = %s" % (a, b) for (a,b) in zip(self.action_names, self.action_names[1:])]
        action_mappings.append("dot(cortex, %s) --> cortex = %s" % (self.action_names[-1], self.action_names[0]))
 
        # Build SPA actions
        actions = spa.Actions(*action_mappings)

        self.bg = spa.BasalGanglia(actions=actions)
        self.thal = spa.Thalamus(self.bg)
        
        #Specify the input
        def start(t):
            if t<0.05: 
                return self.action_names[0]
            else: 
                return '0'

        self.input = spa.Input(cortex=start)



model = Sequence(8, label='Sequence_Module')

with model:
    #Probe things that will be plotted
    pActions = nengo.Probe(model.thal.actions.output, synapse=0.01)
    pUtility = nengo.Probe(model.bg.input, synapse=None)

#Make a simulator and run it
if not spinnaker:
    track = profile("Building", datetime.datetime.now())
    sim = nengo.Simulator(model)
    profile("Building done", track)
else:
    import nengo_spinnaker

    config = nengo_spinnaker.Config()
    for n in model.input.input_nodes.values():
        config[n].f_of_t = True

    sim = nengo_spinnaker.Simulator(model, config=config, machine_name="192.168.1.1")

track = profile("Running", datetime.datetime.now())
sim.run(10.0)
profile("Running done", track)

from matplotlib import pyplot as plt
figure = plt.figure()

p1 = figure.add_subplot(2,1,1)
action_plot = p1.plot(sim.trange(), sim.data[pActions])
p1.set_ylabel('Action')
p1.set_ylim([-0.1, 1.1])
figure.legend(action_plot, model.action_names)

p2 = figure.add_subplot(2,1,2)
p2.plot(sim.trange(), sim.data[pUtility])
p2.set_ylabel('Utility')
p2.set_ylim([-0.1, 1.1])

plt.show(block=True)
