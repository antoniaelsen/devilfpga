from amaranth import Elaboratable, Module, Signal


class NoteWord(Elaboratable):
    """NoteWord

    The TB-303 converts the key (A-G# spanning 5 octaves) to a 6-bit 'note' value, to be passed to the DAC.
    Is this necessary here? No. But we have LUTs so we're doing it anyway.

    A1  = 8  (lowest*)  0V
    C1  = 14
    C2  = 23 (middle C)
    C3  = 35
    C4  = 47
    C5  = 59
    D5# = 62
    E5  = 63 (highest)  3V

    *Apparently the voltage pins this low, until C1

    Parameters
    ----------

    """

    def __init__(self, width: int):
        self.i_slide = Signal()
        self.i_octave = Signal(3)  # 0-4

        self.i_note_a = Signal()  # 0
        self.i_note_a_s = Signal()
        self.i_note_b = Signal()
        self.i_note_c = Signal()
        self.i_note_c_s = Signal()
        self.i_note_d = Signal()
        self.i_note_d_s = Signal()
        self.i_note_e = Signal()
        self.i_note_f = Signal()
        self.i_note_f_s = Signal()
        self.i_note_g = Signal()
        self.i_note_g_s = Signal()  # 11

        self.o_note = Signal(6)

    def elaborate(self, _) -> Module:
        m = Module()

        # Only one note will be high at a time
        #  the output will be the note's value from 0-11, + (octave + 1) * 12 - 4
        m.d.sync += self.o_note.eq(
            self.i_note_a * 0 +
            self.i_note_a_s * 1 +
            self.i_note_b * 2 +
            self.i_note_c * 3 +
            self.i_note_c_s * 4 +
            self.i_note_d * 5 +
            self.i_note_d_s * 6 +
            self.i_note_e * 7 +
            self.i_note_f * 8 +
            self.i_note_f_s * 9 +
            self.i_note_g * 10 +
            self.i_note_g_s * 11 +
            (self.i_octave + 1) * 12 - 4
        )

        return m

    def ports(self):
        return [
            self.i_note_0,
            self.i_note_1,
            self.i_note_2,
            self.i_note_3,
            self.i_note_4,
            self.i_note_5,
            self.i_note_6,
            self.i_note_7,
            self.i_accent,
            self.i_slide,
        ]


class DAC(Elaboratable):
    """CV

    The TB-303 takes a 6-bit output from its microcontroller (whose bits are somewhat erroneously named 'note #'), and through
    a resistor ladder DAC, converts it to a value between 0 and 3V. 

    # TODO(antoniae): confirm range is 0-max
    # TODO(antoniae): slide

    Parameters
    ----------

    """

    def __init__(self, width: int):
        self.i_slide = Signal()
        self.i_note = Signal(6)

        self.o_cv = Signal(width)

        self.width = width

    def elaborate(self, _) -> Module:
        m = Module()

        # C1 = note 14 = 0V
        # E5 = note 63 = 3V (max)
        ceil = 2 ** self.width - 1
        a = ceil / 49
        b = -ceil / (49 * 14)

        m.d.sync += self.o_cv.eq(self.i_note * a + b)

        return m

    def ports(self):
        return [
            self.i_note,
            self.i_slide,
            self.o_cv,
        ]
