from amaranth import Elaboratable, Module, Signal, signed


class LadderFilter(Module):
    def __init__(self, audio_in, audio_out, cutoff_cv, resonance_cv):
        self.audio_in = audio_in
        self.audio_out = audio_out
        self.cutoff_cv = cutoff_cv
        self.resonance_cv = resonance_cv

        # Filter state variables
        self.delay_line = [Signal(signed(16)) for _ in range(4)]
        self.feedback = Signal(signed(16))

        # Calculate filter coefficients
        self.g = (1 - 2 * self.resonance_cv) / (1 + 2 * self.resonance_cv)
        self.alpha = 1 / (1 + 2 * self.resonance_cv)
        self.beta = (1 - self.alpha) / 2

        # Filter processing
        self.comb += self.delay_line[0].eq(self.audio_in +
                                           (self.feedback * self.g))
        self.sync += [self.delay_line[i].eq(self.delay_line[i + 1])
                      for i in range(3)]
        self.comb += self.audio_out.eq(self.delay_line[3])
        self.comb += self.feedback.eq(self.alpha *
                                      (self.audio_in - self.delay_line[3]))


class AntilogConverter(Elaboratable):
    def __init__(self):
        self.i_sig = Signal()
        self.o_sig = Signal()

        self.comb += self.o_sig.eq(((1 << 16) - 1) * (
            1 - ((2 ** 16) - 1) ** (-self.i_sig / ((1 << 16) - 1))))


class Amplifier(Elaboratable):
    def __init__(self, input_signal, output_signal, envelope_cv):
        self.input_signal = input_signal
        self.output_signal = output_signal
        self.envelope_cv = envelope_cv

        self.comb += self.output_signal.eq(self.input_signal *
                                           self.envelope_cv)


class VCF(Elaboratable):
    def __init__(self):
        self.i_audio = Signal()
        self.o_audio = Signal()
        self.cutoff_cv = Signal()
        self.resonance_cv = Signal()
        self.envelope_cv = Signal()

        self.submodules.moog_filter = LadderFilter()
        self.submodules.antilog = AntilogConverter()
        self.submodules.amplifier = Amplifier()

        self.moog_output = Signal(signed(16))
        self.antilog_output = Signal(signed(16))
