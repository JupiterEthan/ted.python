#!/usr/bin/env python

"""
Demos for IAF population time encoding and decoding algorithms.
"""

import sys
import numpy as np

import bionet.utils.gen_test_signal as g
import bionet.utils.test_utils as tu
import bionet.ted.iaf as iaf

# For determining output plot file names:
output_name = 'iaf_pop_demo_'
output_count = 0
output_ext = '.png'

# Define algorithm parameters and input signal:
dur = 0.1
dt = 1e-6
f = 32
bw = 2*np.pi*f
t = np.arange(0, dur, dt)

np.random.seed(0)

noise_power = None
if noise_power == None:
    fig_title = 'IAF input signal with no noise'
else:
    fig_title = 'IAF input signal with %d dB of noise' % noise_power
print fig_title
u = tu.func_timer(g.gen_test_signal)(dur, dt, f, noise_power)
tu.plot_signal(t, u, fig_title,
               output_name + str(output_count) + output_ext)

# Test leaky IAF algorithms:

b1 = 3.5   # bias
d1 = 0.7   # threshold
R1 = 10.0  # resistance
C1 = 0.01  # capacitance

try:
    iaf.iaf_recoverable(u, bw, b1, d1, R1, C1)
except ValueError('reconstruction condition not satisfied'):
    sys.exit()

b2 = 3.4   # bias
d2 = 0.8   # threshold
R2 = 9.0   # resistance
C2 = 0.01  # capacitance

try:
    iaf.iaf_recoverable(u, bw, b2, d2, R2, C2)
except ValueError('reconstruction condition not satisfied'):
    sys.exit()

out_count = 0
out_count += 1
fig_title = 'encoding using leaky IAF algorithm (encoder #1)'
print fig_title
s1 = tu.func_timer(iaf.iaf_encode)(u, dt, b1, d1, R1, C1)
tu.plot_encoded(t, u, s1, fig_title,
                output_name + str(output_count) + output_ext)

out_count += 1
fig_title = 'encoding using leaky IAF algorithm (encoder #2)'
print fig_title
s2 = tu.func_timer(iaf.iaf_encode)(u, dt, b2, d2, R2, C1)
tu.plot_encoded(t, u, s2, fig_title,
                output_name + str(output_count) + output_ext)

out_count += 1
fig_title = 'decoding using leaky IAF population algorithm'
print fig_title
u_rec = tu.func_timer(iaf.iaf_decode_pop)([s1, s2], dur, dt, bw,
                                          [b1, b2], [d1, d2], [R1, R2],
                                          [C1, C2])
tu.plot_compare(t, u, u_rec, fig_title,
                output_name + str(output_count) + output_ext)

# Test nonleaky IAF algorithms:

b1 = 3.5     # bias
d1 = 0.7     # threshold
R1 = np.inf  # resistance
C1 = 0.01    # capacitance

try:
    iaf.iaf_recoverable(u, bw, b1, d1, R1, C1)
except ValueError('reconstruction condition not satisfied'):
    sys.exit()

b2 = 3.4     # bias
d2 = 0.8     # threshold
R2 = np.inf  # resistance
C2 = 0.01    # capacitance

try:
    iaf.iaf_recoverable(u, bw, b2, d2, R2, C2)
except ValueError('reconstruction condition not satisfied'):
    sys.exit()

out_count += 1
fig_title = 'encoding using nonleaky IAF algorithm (encoder #1)'
print fig_title
s1 = tu.func_timer(iaf.iaf_encode)(u, dt, b1, d1, R1, C1)
tu.plot_encoded(t, u, s1, fig_title,
                output_name + str(output_count) + output_ext)

out_count += 1
fig_title = 'encoding using nonleaky IAF algorithm (encoder #2)'
print fig_title
s2 = tu.func_timer(iaf.iaf_encode)(u, dt, b2, d2, R2, C1)
tu.plot_encoded(t, u, s2, fig_title,
                output_name + str(output_count) + output_ext)

out_count += 1
fig_title = 'decoding using nonleaky IAF population algorithm'
print fig_title
u_rec = tu.func_timer(iaf.iaf_decode_pop)([s1, s2], dur, dt, bw,
                                          [b1, b2], [d1, d2], [R1, R2],
                                          [C1, C2])
tu.plot_compare(t, u, u_rec, fig_title,
                output_name + str(output_count) + output_ext)
