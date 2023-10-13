import math
from amaranth import Elaboratable, Memory, Module, Signal

from phase_accumulator import PhaseAccumulator


class Oscillator(Elaboratable):
    """A generic waveform generator.

    Synthesizes a waveform via DDS; a combination of a phase accumulator and lookup table.
    The lookup table is generated using the passed lut_generator function.

    Parameters
    ----------
    f_clk : int
        The clock frequency.
    lut_width : int
        The width in bits of the waveform LUT elements.
    lut_depth : int
        The word count (# of storage elements) of the waveform LUT.
    lut_generator : Function(i: int, width: int, depth: int)
        A function that will generate the values of the waveform LUT.

    """

    def __init__(self,
                 f_clk: int,
                 lut_width: int,
                 lut_depth: int,
                 lut_generator,
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

    def ports(self):
        return [
            self.i_enable,
            self.i_reset,
            self.i_f_target,
            self.o_a,
            self.o_i,
        ]
