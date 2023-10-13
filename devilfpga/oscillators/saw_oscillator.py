import math
from .oscillator import Oscillator

import matplotlib.pyplot as plt

N_SAMPLES_RISING = 7.0 / 9.0


def identity(i: int, width: int, depth: int):
    return math.ceil(i * (2 ** width - 1) / (2 ** depth - 1))


def saw(i: int, width: int, depth: int):
    a = 2.0 ** width
    n_samples = 2 ** depth - 1
    n_rise = min(max(int(N_SAMPLES_RISING * n_samples - 1), 1), n_samples - 1)
    n_fall = n_samples - n_rise

    m = -a / (n_rise - 1.0)
    b = a
    if i >= n_rise:
        m = a / (n_fall + 1.0)
        b = -a / (n_fall + 1.0) * (n_rise - 1.0)

    return math.ceil(m * i + b)


class SawOscillator(Oscillator):
    """A simple sawtooth waveform generator.

    Synthesizes a sawtooth waveform via DDS; a combination of a phase accumulator and lookup table.
    While strictly speaking a LUT is not needed for a sawtooth waveform when using a phase accumulator
    (since the phase accumulates linearly, and the output signal wraps back to 0 when it overflows -- like a saw...),
    a LUT is still used to leave room for potentially simulating quirks from the circuit of the TB-303.

    Parameters
    ----------
    f_clk : int
        The clock frequency.
    lut_width : int
        The width in bits of the waveform LUT elements.
    lut_depth : int
        The word count (# of storage elements) of the waveform LUT.
    """

    def __init__(self, f_clk: int, lut_width: int, lut_depth: int):
        super().__init__(f_clk, lut_width, lut_depth, saw)


def plot_saw_oscillator():
    x = [x for x in range(2 ** 11)]
    y = [saw(y, 8, 11) for y in range(2 ** 11)]

    plt.plot(x, y)
    plt.xlabel('i')
    plt.ylabel('Amplitude')
    plt.title('Saw')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    plot_saw_oscillator()
