import math
from amaranth.sim import Simulator
from ...oscillators.phase_accumulator import PhaseAccumulator


def test_phase_accumulator():
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
