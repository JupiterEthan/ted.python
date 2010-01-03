#!/usr/bin/env python

"""
Demos of time encoding and decoding algorithms that use spline
interpolation with IAF neurons.
"""

import sys
import numpy as np

import bionet.utils.gen_test_signal as g
import bionet.utils.test_utils as tu
import bionet.ted.iaf as iaf

# For determining output plot file names:
output_name = 'iaf_spline_demo_'
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
    fig_title = 'IAF input signal with no noise';
else:
    fig_title = 'IAF input signal with %d dB of noise' % noise_power;
print fig_title
u = tu.func_timer(g.gen_test_signal)(dur, dt, f, noise_power)
tu.plot_signal(t, u, fig_title,
               output_name + str(output_count) + output_ext)

b = 3.5   # bias
d = 0.7   # threshold
R = 10.0  # resistance
C = 0.01  # capacitance

try:
    iaf.iaf_recoverable(u, bw, b, d, R, C)
except ValueError('reconstruction condition not satisfied'):
    sys.exit()

# Test leaky algorithms:

output_count += 1
fig_title = 'encoding using leaky IAF algorithm'
print fig_title
s = tu.func_timer(iaf.iaf_encode)(u, dt, b, d, R, C)
tu.plot_encoded(t, u, s, fig_title,
                output_name + str(output_count) + output_ext)

output_count += 1
fig_title = 'decoding using leaky spline-based IAF algorithm'
print fig_title
u_rec = tu.func_timer(iaf.iaf_decode_spline)(s, dur, dt, b, d, R, C)
tu.plot_compare(t, u, u_rec, fig_title,
                output_name + str(output_count) + output_ext)

# Test nonleaky algorithms:

R = np.inf

output_count += 1
fig_title = 'encoding using nonleaky IAF algorithm'
print fig_title
s = tu.func_timer(iaf.iaf_encode)(u, dt, b, d, R, C)
tu.plot_encoded(t, u, s, fig_title,
                output_name + str(output_count) + output_ext)

output_count += 1
fig_title = 'decoding using nonleaky spline-based IAF algorithm'
print fig_title
u_rec = tu.func_timer(iaf.iaf_decode_spline)(s, dur, dt, b, d, R, C)
tu.plot_compare(t, u, u_rec, fig_title,
                output_name + str(output_count) + output_ext)
