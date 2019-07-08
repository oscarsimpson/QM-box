import matplotlib.pyplot as plt
import numpy as np
import config
import decomposition as decomp


def main():
    print("Hello World")
    plt.rcParams['toolbar'] = 'None'
    function = config.wavefunction

    # Initial wavefunction
    plt.subplot(2, 1, 1)
    xs = np.linspace(*config.potential(0), config.FIDELITY)
    ys = [function(x) for x in xs]
    plt.plot(xs, ys)

    # Decompose, time evolve
    coeffs = decomp.decompose(function, config.potential(0))
    func = decomp.recompose(coeffs, config.potential(0))

    # Draw
    plt.subplot(2, 1, 2)
    xs = np.linspace(*config.potential(0), config.FIDELITY)
    ys = [func(x) for x in xs]
    plt.plot(xs, ys)

    plt.show()

    # while():
        # increment time
        # decompose 'func' into new potential ->'ys'
        # time evolve 'ys' -> recompose -> 'func'
        # draw


if __name__ == "__main__":
    main()
