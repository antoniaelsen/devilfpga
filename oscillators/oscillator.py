import math
from amaranth import Elaboratable, Memory, Module, Signal

from phase_accumulator import PhaseAccumulator


class Oscillator(Elaboratable):
    """
    A generic waveform generator
    """

    def __init__(self,
                 f_clk,             # clock frequency
                 lut_width,         # LUT value size
                 lut_depth,         # LUT word count
                 lut_generator,     # LUT value generator
                 ):
        self.f_clk = f_clk
        self.lut_width = lut_width
        self.memory_addr_width = math.ceil(math.log2(lut_depth))
        self.phase_acc_width = 32

        self.i_enable = Signal()
        self.i_reset = Signal()
        self.i_f_target = Signal(16)

        self.o_a = Signal(lut_width)
        self.o_i = Signal(lut_width)

        lut = [lut_generator(x, lut_width, self.memory_addr_width)
               for x in range(lut_depth)]
        self.memory = Memory(width=lut_width, depth=lut_depth, init=lut)

    def elaborate(self, _) -> Module:
        m = Module()

        m.submodules.phase_acc = phase_acc = PhaseAccumulator(
            self.f_clk,
            self.memory_addr_width,
        )

        m.d.sync += [
            phase_acc.i_enable.eq(self.i_enable),
            phase_acc.i_reset.eq(self.i_reset),
            phase_acc.i_f_target.eq(self.i_f_target)
        ]

        m.d.comb += [
            self.o_a.eq(phase_acc.o_i),
            self.o_i.eq(phase_acc.o_i)
        ]

        return m
