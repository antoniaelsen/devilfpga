from amaranth.sim import Simulator

from oscillator import Oscillator


def identity(i, width, depth):
    return i * (2 ** width - 1) / (2 ** depth - 1)


class SawOscillator(Oscillator):
    """
    A sawtooth waveform generator

    The waveform is synthesized via DDS; a combination of a phase accumulator and lookup table.
    While strictly speaking a LUT is not needed for a sawtooth waveform when using a phase accumulator
    (since the phase accumulates linearly...), a LUT is still used in order to simulate the (inconsistencies / harmonics)
    of the analog waveform in the TR-303.
    """

    def __init__(self, f_clk, lut_width, lut_depth):
        super().__init__(f_clk, lut_width, lut_depth, identity)


if __name__ == "__main__":
    # acc_width = 11
    # f_clk = 100_000_000
    # f_target = 440
    # inc = 18897
    # n_cycles = math.ceil(2 ** 32 / inc)

    # dut = SawOscillator(f_clk, acc_width)
    # sim = Simulator(dut)
    # sim.add_clock(1e-8)

    # def bench():
    #     yield dut.i_reset.eq(1)
    #     yield

    #     yield dut.i_reset.eq(0)
    #     yield dut.i_enable.eq(1)
    #     yield dut.i_f_target.eq(f_target)
    #     yield
    #     yield
    #     yield
    #     yield

    #     assert (yield dut.o_i) == 0
    #     assert (yield dut.o_a) == 0

    #     for _ in range(n_cycles):
    #         yield

    #     assert (yield dut.o_i) == 2 ** acc_width - 1

    # sim.add_sync_process(bench)
    # with sim.write_vcd("saw_oscillator.vcd"):
    #     sim.run()
