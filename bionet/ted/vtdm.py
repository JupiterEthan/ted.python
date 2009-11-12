#!/usr/bin/env python

"""
Block-based time decoding algorithm used by real-time time decoding algorithm.
"""

__all__ = ['asdm_decode_vander', 'asdm_decode_vander_ins',
           'iaf_decode_vander']

from numpy import arange, asarray, conjugate, cumsum, diag, diff, dot, \
     exp, fliplr, float, imag, isinf, newaxis, nonzero, ones, real, \
     reshape, shape, sin, triu, vander, zeros

from bionet.utils.numpy_extras import mdot
import bionet.ted.bpa as bpa

def asdm_decode_vander(s, dur, dt, bw, b, d, k, sgn=-1):
    """Decode a finite length signal encoded by an asynchronous
    sigma-delta modulator by solving a Vandermonde system using BPA.

    Parameters
    ----------
    s: numpy array of floats
        Encoded signal. The values represent the time between spikes (in s).
    dur: float
        Duration of signal (in s).
    dt: float
        Sampling resolution of original signal; the sampling frequency
        is 1/dt Hz.
    bw: float
        Signal bandwidth (in rad/s).
    b: float
        Encoder bias.
    d: float
        Encoder threshold.
    k: float
        Encoder integration constant.
    sgn: {-1,1}
        Sign of first spike.

    """

    # Since the compensation principle uses the differences between
    # spikes, the last spike must effectively be dropped:
    s = asarray(s)
    ts = cumsum(s)
    ns = len(s)-1
    n = ns-1               # corresponds to N in Prof. Lazar's paper

    # Create the vectors and matricies needed to obtain the
    # reconstruction coefficients:
    z = exp(1j*2*bw*ts[:-1]/n)

    V = fliplr(vander(z))  # pecularity of numpy's vander() function
    P = triu(ones((ns, ns), float))
    D = diag(exp(1j*bw*ts[:-1]))

    # Compute the quanta:
    if sgn == -1:
        q = asarray([(-1)**i for i in xrange(0, ns)])*(2*k*d-b*s[1:])
    else:
        q = asarray([(-1)**i for i in xrange(1, ns+1)])*(2*k*d-b*s[1:])
        
    # Obtain the reconstruction coefficients by solving the
    # Vandermonde system using BPA:
    d = bpa.bpa(V, mdot(D, P, q[:, newaxis]))

    # Reconstruct the signal:
    t = arange(0, dur, dt)
    u = zeros(len(t), float)
    for i in xrange(ns):
        c = 1j*(bw-i*2*bw/n)
        u += c*d[i]*exp(-c*t)

    return u

def asdm_decode_vander_ins(s, dur, dt, bw, b, sgn=-1):
    """Decode a finite length signal encoded by an asynchronous sigma-delta
    modulator by solving a parameter-insensitive Vandermonde system
    using BPA.

    Parameters
    ----------
    s: numpy array of floats
        Encoded signal. The values represent the time between spikes (in s).
    dur: float
        Duration of signal (in s).
    dt: float
        Sampling resolution of original signal; the sampling frequency
        is 1/dt Hz.
    bw: float
        Signal bandwidth (in rad/s).
    b: float
        Encoder bias.
    sgn: {-1,1}
        Sign of first spike.
        
    """

    # Since the compensation principle uses the differences between
    # spikes, the last spike in s must effectively be dropped:
    s = asarray(s)
    ts = cumsum(s)
    ns = len(s)-1
    n = ns-1               # corresponds to N in Prof. Lazar's paper
    
    # Create the vectors and matricies needed to obtain the
    # reconstruction coefficients:
    z = exp(1j*2*bw*ts[:-1]/n)
    V = fliplr(vander(z))  # pecularity of numpy's vander() function
    D = diag(exp(1j*bw*ts[:-1]))
    P = triu(ones((ns, ns), float))

    a = zeros(ns, float)
    a[::-2] = 1.0
    a = a[:, newaxis]      # column vector

    bh = zeros(ns, float)
    bh[-1] = 1.0
    bh = bh[newaxis]       # row vector

    ex = ones(ns, float)
    if sgn == -1:
        ex[0::2] = -1.0
    else:
        ex[1::2] = -1.0
    r = (ex*s[1:])[:, newaxis] 

    # Solve the Vandermonde systems using BPA:
    ## Observation: constructing P-dot(a,bh) directly without
    ## creating P, a, and bh separately does not speed this up
    x = bpa.bpa(V, mdot(D, P-dot(a, bh), r))
    y = bpa.bpa(V, dot(D, a))

    # Compute the coefficients:
    d = b*(x-mdot(y, conjugate(y.T), x)/dot(conjugate(y.T), y))
    
    # Reconstruct the signal:
    t = arange(0, dur, dt)
    u = zeros(len(t), float)
    for i in xrange(ns):
        c = 1j*(bw-i*2*bw/n)
        u += c*d[i]*exp(-c*t)

    return u

def iaf_decode_vander(s, dur, dt, bw, b, d, R, C):
    """Decode a finite length signal encoded by an integrate-and-fire
    neuron by solving a Vandermonde system using BPA.

    Parameters
    ----------
    s: numpy array of floats
        Encoded signal. The values represent the time between spikes (in s).
    dur: float
        Duration of signal (in s).
    dt: float
        Sampling resolution of original signal; the sampling frequency
        is 1/dt Hz.
    bw: float
        Signal bandwidth (in rad/s).
    b: float
        Encoder bias.
    d: float
        Encoder threshold.
    R: float
        Neuron resistance.
    C: float
        Neuron capacitance.

    """

    # Since the compensation principle uses the differences between
    # spikes, the last spike must effectively be dropped:
    s = asarray(s)
    ts = cumsum(s)
    ns = len(s)-1
    n = ns-1               # corresponds to N in Prof. Lazar's paper

    # Create the vectors and matricies needed to obtain the
    # reconstruction coefficients:
    z = exp(1j*2*bw*ts[:-1]/n)

    V = fliplr(vander(z))  # pecularity of numpy's vander() function
    P = triu(ones((ns, ns), float))
    D = diag(exp(1j*bw*ts[:-1]))

    # Compute the quanta:
    if isinf(R):
        q = asarray(C*d-b*s[1:])
    else:
        q = asarray(C*(d+b*R*(exp(-s[1:]/(R*C))-1)))
        
    # Obtain the reconstruction coefficients by solving the
    # Vandermonde system using BPA:
    d = bpa.bpa(V, mdot(D, P, q[:, newaxis]))

    # Reconstruct the signal:
    t = arange(0, dur, dt)
    u = zeros(len(t), float)
    for i in xrange(ns):
        c = 1j*(bw-i*2*bw/n)
        u += c*d[i]*exp(-c*t)

    return u