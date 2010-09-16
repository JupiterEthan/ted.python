#!/usr/bin/env python

"""
Generate a bandlimited test signal.
"""

import numpy as np

# Set matplotlib backend so that plots can be generated without a
# display:
import matplotlib
matplotlib.use('AGG')

from bionet.utils.misc import func_timer
import bionet.utils.plotting as pl
import bionet.utils.gen_test_signal as g

# For determing output plot file names:
output_name = 'gen_test_signal_demo_'
output_count = 0
output_ext = '.png'

print 'creating test signal..'
dur = 1.0
fs = 1e4
dt = 1.0/fs
f = 10
t = np.arange(0, dur, dt)

np.random.seed(0)
out_count = 0
fig_title = 'test signal with no noise'
print fig_title
u = func_timer(g.gen_test_signal)(dur, dt, f)
pl.plot_signal(t, u, fig_title,
               output_name + str(output_count) + output_ext)

np.random.seed(0)
output_count += 1
noise_power = 1
fig_title = 'test signal with %d dB of noise' % noise_power
print fig_title
u = func_timer(g.gen_test_signal)(dur, dt, f, noise_power)
pl.plot_signal(t, u, fig_title,
               output_name + str(output_count) + output_ext)

np.random.seed(0)
output_count += 1
noise_power = -5
fig_title = 'test signal with %d dB of noise' % noise_power
print fig_title
u = func_timer(g.gen_test_signal)(dur, dt, f, noise_power)
pl.plot_signal(t, u, fig_title,
               output_name + str(output_count) + output_ext)

np.random.seed(0)
output_count += 1
noise_power = -5
nc = 8
fig_title = 'test signal with %d dB of noise and %i components' % \
            (noise_power, nc)
print fig_title
u = func_timer(g.gen_test_signal)(dur, dt, f, noise_power, nc)
pl.plot_signal(t, u, fig_title,
               output_name + str(output_count) + output_ext)

np.random.seed(0)
output_count += 1
f = 50
noise_power = -10
nc = 20
fig_title = 'test signal with %d dB of noise and %i components' % \
            (noise_power, nc)
print fig_title
u = func_timer(g.gen_test_signal)(dur, dt, f, noise_power, nc)
pl.plot_signal(t, u, fig_title,
               output_name + str(output_count) + output_ext)
