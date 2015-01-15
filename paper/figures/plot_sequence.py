import datetime
import nengo
import nengo.spa as spa
import plot_settings
import seaborn as sns
from matplotlib import pyplot as plt

dimensions = 16

class Sequence(spa.SPA):
    def __init__(self):
        spa.SPA.__init__(self)
        
        #Specify the modules to be used
        self.cortex = spa.Buffer(dimensions=dimensions)
        
        # Generate sequential action names
        self.action_names = [chr(ord("A") + i) for i in range(4)]
      
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



model = Sequence(label='Sequence_Module')

with model:
    #Probe things that will be plotted
    pActions = nengo.Probe(model.thal.actions.output, synapse=0.01)
    pUtility = nengo.Probe(model.bg.input, synapse=None)

sim = nengo.Simulator(model)

sim.run(0.5)
sns.set_palette("colorblind")
figure, axis = plt.subplots(figsize=(plot_settings.column_width, 3.5), frameon=False)

action_plot = axis.plot(sim.trange(), sim.data[pActions])
axis.set_xlabel("Time / s")
axis.set_ylabel("Action")
axis.set_ylim([-0.1, 1.1])
figure.legend(action_plot, model.action_names, ncol=2)

plt.show(block=True)

# Save figure
figure.tight_layout(pad=0.0)
figure.savefig("sequence.pdf")