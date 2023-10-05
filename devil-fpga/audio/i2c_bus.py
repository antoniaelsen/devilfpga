from amaranth import ClockDomain, ClockSignal, Elaboratable, Module, Signal
from amaranth.sim import Simulator


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


# Instantiate the simulator and run the test bench
if __name__ == "__main__":
    dut = I2CBus()
    sim = Simulator(dut)
    sim.add_clock(1 / (48000 * 256))

    def bench():
        yield dut.mclk.eq(0)
        yield dut.lrclk.eq(0)
        yield dut.o_audio.eq(0)
        yield
        assert (yield dut.o_audio) == 0

        yield dut.mclk.eq(1)

        for _ in range(64):  # 64 SCLK cycles per sample
            yield dut.aud_adc.eq(0xABCD)  # Simulated audio data
            yield

            # Check if audio output is as expected
            if (yield dut.lrclk):
                # Right channel
                # Check audio data for right channel
                assert (yield dut.o_audio) == 0xABCD
            else:
                # Left channel
                # Check audio data for left channel
                assert (yield dut.o_audio) == 0xABCD

    sim.add_sync_process(bench)
    with sim.write_vcd("saw_oscillator.vcd"):
        sim.run()
