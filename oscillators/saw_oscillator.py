import math
from amaranth.sim import Simulator
from amaranth import Elaboratable, Module, Signal

from phase_accumulator import PhaseAccumulator


class SawOscillator(Elaboratable):
    """
    A saw waveform generator
    """

    def __init__(self, f_clk, output_width):
        self.phase_acc_width = 32
        self.output_width = output_width

        self.i_enable = Signal()
        self.i_reset = Signal()
        self.i_f_target = Signal(16)

        self.o_a = Signal(output_width)
        self.o_i = Signal(output_width)

        self.f_clk = f_clk

    def elaborate(self, _) -> Module:
        m = Module()

        m.submodules.phase_acc = phase_acc = PhaseAccumulator(
            self.f_clk,
            self.output_width
        )
        m.d.sync += [
            phase_acc.i_enable.eq(self.i_enable),
            phase_acc.i_reset.eq(self.i_reset),
            phase_acc.i_f_target.eq(self.i_f_target)
        ]

        m.d.sync += [
            self.o_a.eq(phase_acc.o_i),
            self.o_i.eq(phase_acc.o_i)
        ]

        return m


if __name__ == "__main__":
    acc_width = 11
    f_clk = 100_000_000
    f_target = 440
    inc = 18897
    n_cycles = math.ceil(2 ** 32 / inc)

    dut = SawOscillator(f_clk, acc_width)
    sim = Simulator(dut)
    sim.add_clock(1e-8)

    def bench():
        yield dut.i_reset.eq(1)
        yield

        yield dut.i_reset.eq(0)
        yield dut.i_enable.eq(1)
        yield dut.i_f_target.eq(f_target)
        yield
        yield
        yield
        yield

        assert (yield dut.o_i) == 0
        assert (yield dut.o_a) == 0

        for _ in range(n_cycles):
            yield

        assert (yield dut.o_i) == 2 ** acc_width - 1

    sim.add_sync_process(bench)
    with sim.write_vcd("saw_oscillator.vcd"):
        sim.run()
