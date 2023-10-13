import math
from amaranth.sim import Simulator
from ...oscillators.saw_oscillator import SawOscillator, saw

import matplotlib.pyplot as plt


def test_saw():
    n_samples = 2 ** 11
    peak = min(max(int((7.0 / 9.0) * n_samples - 1), 1), n_samples - 1)
    print(
        f"peak: {peak}")
    print(
        f"peak: {peak}, half_peak: {math.ceil(peak / 2)}, halfpeak saw: {saw(math.ceil(peak / 2), 8, 11)}")
    assert saw(0, 8, 11) == 0.0
    assert saw(math.ceil(peak / 2), 8, 11) == 0.5
    assert saw(peak, 8, 11) == 1.0
    assert saw(n_samples - 1, 8, 11) == 0.0


def test_saw_oscillator():
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
