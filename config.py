import numpy as np


FFT_NUM = 15
TIMESTEP = 1
ZERO_EPS = 10**(-10)
FIDELITY = 1000


def potential(t):
    """Return the boundaries of the infinite potential as a tuple."""
    return(-1, 2*np.pi+-1)


def wavefunction(x):
    """Return the initial value of the wavefunction at x."""
    x0 = potential(0)[0]
    x1 = potential(0)[1]
    if x0 < x < x1:
        return(np.sin(1.1*(x+1)))
    else:
        return(0)


def clean(arr):
    """Set all small elements of a complex array to zero.

    Each element is checked against ZERO_EPS and if it is smaller then the
    value is set to zero. This is useful for printing arrays so that small
    floats are clearly seen as zero.
    """
    index = 0
    while index < len(arr):
        if np.abs(arr[index]) < ZERO_EPS:
            arr[index] = 0
        elif np.abs(np.imag(arr[index])) < ZERO_EPS:
            arr[index] = np.real(arr[index])
        elif np.abs(np.real(arr[index])) < ZERO_EPS:
            arr[index] = 1j*np.imag(arr[index])
        index += 1
    return(arr)


def oddify(function, x, x0=0):
    """Convert a function on positive reals to an odd function over reals.

    Optional parameter x0 specifies the location around which the new
    function is odd.
    """
    # This is used so that whatever our function is, the basis is purely in
    # terms of sinusoids
    if x < x0:
        out = -function(2*x0-x)
    else:
        out = function(x)
    return(out)
