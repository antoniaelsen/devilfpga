from amaranth import Elaboratable, Module, Signal


class I2CBus(Elaboratable):
    """I2C audio bus controller.

    Parameters
    ----------
    f_clk : int
        The clock frequency.
    f_dac_clk : int
        The clock frequency of the DAC.
    output_width : int
        The width in bits of the audio output (per channel).
    n_channels : int

    """

    def __init__(self,
                 f_clk: int = 480000,
                 f_dac_clk: int = 480000 * 64,
                 output_width: int = 16,
                 n_channels: int = 2,
                 ):

        self.i_audio = Signal()                 # data output to speakers
        self.o_audio = Signal(name="aud_dac")   # data output to speakers (PCM)
        self.lrclk = Signal(name="aud_lrck")    # L/R / word-select clock
        self.mclk = Signal(name="aud_mclk")     # master clock
        self.sclk = Signal(name="aud_sclk")     # serial clock / bit clock

        self.f_mclk = f_clk * 256
        self.f_sclk = f_dac_clk

    def elaborate(self, platform):
        m = Module()

        # Generate MCLK (Master Clock)
        m.domains.sync += self.mclk.eq(1)
        m.d.sync += self.mclk.eq(~self.mclk)

        # Generate SCLK (Serial Clock)
        sclk_counter = Signal(range(int(self.f_mclk / self.f_sclk)))
        with m.If(sclk_counter == 0):
            m.d.sync += sclk_counter.eq(sclk_counter.reset)
            m.d.sync += self.sclk.eq(~self.sclk)
        with m.Else():
            m.d.sync += sclk_counter.eq(sclk_counter + 1)

        # Output data on the rising edge of SCLK
        with m.If(self.sclk):
            m.d.sync += self.o_audio.eq(self.aud_adc)

        lrclk_counter = Signal(range(2))

        # Left
        with m.If(lrclk_counter == 0):
            m.d.sync += lrclk_counter.eq(lrclk_counter + 1)
            m.d.sync += self.lrclk.eq(0)
        # Right
        with m.Else():
            m.d.sync += lrclk_counter.eq(lrclk_counter.reset)
            m.d.sync += self.lrclk.eq(1)

        return m

    def ports(self):
        return [
            self.i_audio,
            self.o_audio,
            self.lrclk,
            self.mclk,
            self.sclk,
        ]
