import math
from amaranth.sim import Simulator
from amaranth import Elaboratable, Module, Signal


class PhaseAccumulator(Elaboratable):
    """
    A phase accumulator for DDS.

    The phase accumulator is a counter that is incremented by a phase increment
    value. The increment is informed by the target frequency, the clock frequency,
    and the resolution of the phase accumulator, such that incrementing the phase
    accumulator every clock cycle will sample a LUT to generate a waveform that
    oscillates at the target frequency.
    """

    def __init__(self,
                 f_clk,
                 output_width
                 ):
        self.output_width = output_width
        self.phase_acc_width = 32

        self.i_enable = Signal()
        self.i_reset = Signal()
        self.i_f_target = Signal(16)

        self.o_inc = Signal(self.phase_acc_width)
        self.o_i = Signal(output_width)

        self.s_phase_acc = Signal(self.phase_acc_width)

        self.f_clk = f_clk

    def __repr__(self):
        print(f"< PhaseAccumulator >")

    def elaborate(self, _) -> Module:
        """
        To achieve a target frequency Ft,
            given a clock frequency Fc,
            and an accumulator bit depth of d;

            inc = (Ft * 2 ** d) / Fc
        """
        m = Module()

        with m.If(self.i_reset):
            m.d.sync += self.s_phase_acc.eq(0)

        with m.Elif(self.i_enable):
            m.d.comb += self.o_inc.eq((self.i_f_target *
                                       (1 << self.phase_acc_width)) // self.f_clk)

            m.d.comb += self.o_i.eq(self.s_phase_acc[-self.output_width:])

        m.d.sync += self.s_phase_acc.eq(self.s_phase_acc + self.o_inc)

        return m


if __name__ == "__main__":
    f_clk = 100_000_000
    f_target = 440
    inc = 18897
    output_width = 11
    n_cycles = math.ceil(2 ** 32 / inc)

    dut = PhaseAccumulator(f_clk, output_width)
    sim = Simulator(dut)
    sim.add_clock(1 / f_clk)

    def bench():
        yield dut.i_reset.eq(1)
        yield

        yield dut.i_reset.eq(0)
        yield dut.i_enable.eq(1)
        yield dut.i_f_target.eq(f_target)
        yield

        assert (yield dut.o_inc) == inc
        assert (yield dut.o_i) == 0

        for i in range(n_cycles - 1):
            yield

        assert (yield dut.o_i) == 2 ** output_width - 1

        yield

        assert (yield dut.o_i) == 0

    sim.add_sync_process(bench)
    with sim.write_vcd("phase_accumulator.vcd"):
        sim.run()
