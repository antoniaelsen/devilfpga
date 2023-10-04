import math
from amaranth.sim import Simulator
from oscillator import Oscillator


def identity(i: int, width: int, depth: int):
    return math.ceil(i * (2 ** width - 1) / (2 ** depth - 1))


class SawOscillator(Oscillator):
    """A sawtooth waveform generator.

    Synthesizes a sawtooth waveform via DDS; a combination of a phase accumulator and lookup table.
    While strictly speaking a LUT is not needed for a sawtooth waveform when using a phase accumulator
    (since the phase accumulates linearly, and the output signal wraps back to 0 when it overflows -- like a saw...),
    a LUT is still used to leave room for simulating quirks from the circuit of the TB-303.

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
        super().__init__(f_clk, lut_width, lut_depth, identity)


if __name__ == "__main__":
    lut_width = 8
    lut_depth = 2 ** 11
    f_clk = 100_000_000
    f_target = 440
    inc = 18897
    n_cycles = math.ceil(2 ** 32 / inc)

    dut = SawOscillator(f_clk, lut_width, lut_depth)
    sim = Simulator(dut)
    sim.add_clock(1 / f_clk)

    def bench():
        yield dut.i_reset.eq(1)
        yield

        yield dut.i_reset.eq(0)
        yield dut.i_enable.eq(1)
        yield dut.i_f_target.eq(f_target)
        yield
        yield

        assert (yield dut.o_i) == 0
        assert (yield dut.o_a) == 0

        for _ in range(n_cycles - 1):
            yield

        assert (yield dut.o_i) == 2 ** lut_width - 1

        yield

        assert (yield dut.o_i) == 0

    sim.add_sync_process(bench)
    with sim.write_vcd("saw_oscillator.vcd"):
        sim.run()
