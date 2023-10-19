from amaranth.sim import Delay, Settle, Simulator
from ...modules.vco import Antilog


def test_antilog():
    dut = Antilog(16)
    sim = Simulator(dut)

    def bench():
        # C1 = 0    = 130.81 Hz
        # E5 = max  = 2637.02 Hz

        yield dut.i_cv.eq(0)
        yield Delay(1e-6)
        yield Settle()
        assert (yield dut.o_f) == 131

        yield dut.i_cv.eq(2 ** 16 - 1)
        yield Delay(1e-6)
        yield Settle()
        assert (yield dut.o_f) == 2637

    sim.add_process(bench)
    with sim.write_vcd("vco.vcd"):
        sim.run()
