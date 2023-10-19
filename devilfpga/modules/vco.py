from amaranth import Elaboratable, Module, Signal

from ..oscillators.saw_oscillator import SawOscillator
from ..oscillators.square_oscillator import SquareOscillator


class Antilog(Elaboratable):
    """Antilog

    Parameters
    ----------
    width : int
        The width in bits of the CV.

    """

    def __init__(self, width: int):
        self.i_cv = Signal(width)
        self.o_f = Signal(16)

        self.width = width

    def elaborate(self, _) -> Module:
        m = Module()

        # C1 = 0    = 130.81 Hz
        # E5 = max  = 2637.02 Hz
        ceil = 2 ** self.width - 1
        m.d.comb += self.o_f.eq(self.i_cv * (2637 - 131) // ceil + 131)

        return m

    def ports(self):
        return [
            self.i_cv,
            self.o_f,
        ]


class VCO(Elaboratable):
    """VCO

    Parameters
    ----------


    """

    def __init__(self, width: int):
        self.i_cv = Signal(width)
        self.i_waveform = Signal()  # 0 = saw, 1 = square
        self.o_a = Signal(width)

        self.width = width

    def elaborate(self, _) -> Module:
        m = Module()

        f_clk = 100_000_000
        lut_width = 8
        lut_depth = 2 ** 11

        m.submodule.antilog = antilog = Antilog(self.width)
        m.submodule.nco_saw = nco_saw = SawOscillator(
            f_clk,
            lut_width,
            lut_depth,
        )
        m.submodule.nco_sqr = nco_sqr = SquareOscillator(
            f_clk,
            lut_width,
            lut_depth,
        )

        f = Signal(16)

        m.d.comb += antilog.i_cv.eq(self.i_cv)
        m.d.comb += f.eq(antilog.o_f)

        m.d.comb += [
            nco_saw.i_enable.eq(1),
            nco_saw.i_f_target.eq(f),
            nco_sqr.i_enable.eq(1),
            nco_sqr.i_f_target.eq(f)
        ]

        with m.If(self.i_waveform == 0):
            m.d.comb += self.o_a.eq(nco_saw.o_a)

        with m.Elif(self.i_waveform == 1):
            m.d.comb += self.o_a.eq(nco_sqr.o_a)

        return m

    def ports(self):
        return [
            self.i_cv,
            self.i_waveform,
            self.o_a,
        ]
