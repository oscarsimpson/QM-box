import numpy as np
import config


def decompose(function, potential):
    """Return Fourier coeffs of 'function' over the 'potential' interval."""
    x0 = potential[0]
    x1 = potential[1]
    xs = np.linspace(x0-x1, x1-x0, 2*config.FFT_NUM, False)
    ys = [config.oddify(function, x+x0, x0) for x in xs]
    # This is the sampled function shifted so that it is centred at 0, ie the
    # basis functions should all be sinusoids.
    # If the potential has expanded, function(x>=x1) still reads as 0
    # If the potential has shrunk, ys is only computed up to x1
    Es = np.fft.fft(ys)
    # Now we renormalise, in the case of a shrunk potential, and due to
    # sampling
    power = np.sqrt(np.abs(Es)**2).sum()
    i = 0
    while(i < len(Es)):
        # Not sure why we need the alternating -1 but it makes it work
        Es[i] = (-1)**(i+1) * -1j * Es[i]/power
        i += 1
    return np.fft.fftshift(Es)
    # -j is used as we have (exp(jx)-exp(-jx))/2j


def recomposete(coeffs, potential):
    """Return the time evolved wavefunction.

    Take a set of Fourier coeffs and the potential, and calculates the value
    of the wavefunction at the next timestep, using the current basis
    functions.
    """

    def func(x):
        value = 0
        n = 0
        while(n < len(coeffs)//2):
            value += coeffs[n+len(coeffs)//2]*basis(n, potential)(x)\
                * np.exp(1j * n * config.TIMESTEP)
            n += 1
        return value
    return func


def recompose(coeffs, potential):
    """Return the non-time evolved wavefunction.

    Take a set of Fourier coeffs and the potential, and calculates the value
    of the wavefunction at this timestep, using the current basis functions.
    """

    def func(x):
        value = 0
        n = 0
        while(n < len(coeffs)//2):
            value += coeffs[n+len(coeffs)//2]*basis(n, potential)(x)
            n += 1
        return value
    return func


def basis(n, potential):
    """Return nth basis function within the infinite potential specified."""
    x0 = potential[0]
    x1 = potential[1]

    def func(x):
        if x0 < x < x1:
            return(np.sin(np.pi*(x-x0)*n/(x1-x0)))
            # The x-x0 is to complement the shift to start at 0 of ys above.
        else:
            return(0)
    return func
