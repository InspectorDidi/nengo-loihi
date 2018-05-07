import nengo
import nengo_loihi

import matplotlib.pyplot as plt


with nengo.Network(seed=1) as model:
    u = nengo.Node(output=0.5)
    up = nengo.Probe(u)

    a = nengo.Ensemble(100, 1, label='a',
                       max_rates=nengo.dists.Uniform(100, 120),
                       intercepts=nengo.dists.Uniform(-0.5, 0.5))
    ac = nengo.Connection(u, a, synapse=None)
    ap = nengo.Probe(a)

    b = nengo.Ensemble(101, 1, label='b',
                       max_rates=nengo.dists.Uniform(100, 120),
                       intercepts=nengo.dists.Uniform(-0.5, 0.5))
    nengo.Connection(a, b)
    # nengo.Connection(a, b, solver=nengo.solvers.LstsqL2(weights=True))
    bp = nengo.Probe(b)


# with nengo.Simulator(model) as sim:
with nengo_loihi.Simulator(model, target='sim') as sim:
    sim.run(0.5)


output_filter = nengo.synapses.Alpha(0.02)
plt.plot(sim.trange(), output_filter.filtfilt(sim.data[up]))
plt.plot(sim.trange(), output_filter.filtfilt(sim.data[ap]))
plt.plot(sim.trange(), output_filter.filtfilt(sim.data[bp]))

plt.show()
