from amaranth import Elaboratable, Module, Signal


class PhaseAccumulator(Elaboratable):
    """A phase accumulator for DDS.
    """

    def __init__(self, f_clk: int, output_width: int):
        self.output_width = output_width
        self.phase_acc_width = 32

        self.i_enable = Signal()
        self.i_reset = Signal()
        self.i_f_target = Signal(16)

        self.o_inc = Signal(self.phase_acc_width)
        self.o_i = Signal(output_width)

        self.s_phase_acc = Signal(self.phase_acc_width)

        self.f_clk = f_clk

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

    def ports(self):
        return [
            self.i_enable,
            self.i_reset,
            self.i_f_target,
            self.o_inc,
            self.o_i,
        ]
