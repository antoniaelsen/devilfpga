# FPGACID

A recreation of the Roland TB-303 synthesizer on an FPGA. Why? Because.
Targeting the FPGA in the Analogue Pocket (Altera Cyclone V ACM-027-A4?), packaging the build as an OpenFPGA core. [Amaranth](https://amaranth-lang.org/docs/amaranth/latest/cover.html) HDL.

Omitting the sequencer, for now. Accent and glide seem crucial, so hopefully, soon(tm).

## Installation

### Requirements

- python 3, pip
- cython or pypy

Testing

- gtkwave

## TB-303 Design

(Below is my understanding of the TB-303's schematic. I am not an EE. If you know better, I'd love to hear from you :))

### Modules

- VCO
  - The VCO supports both a sawtooth and square wave.
  - The sawtooth wave is generated 'directly' (Q28).
  - The square wave is generated by passing the saw through a waveshaper (Q8) (allegedly).
- VCF
  - The filter consists of a low-pass ladder filter.
  - 24dB low-pass 4-pole resonant filter
  - Resonance - TBD
  - Decay - TBD
  - VCF Trim - TBD
  - The envelope generator drives te VCF.
- VCA
  - The envelope generator drives the VCA as well.
- Envelope Generator
  - The envelope generator only modulates decay, no attack / sustain / release.
- Mixer

## FPGA Implementation

### Waveforms

Waveforms are implemented via direct digital synthesis (DDS); the waveform is stored as discrete amplitude values in a waveform LUT, and a phase accumulator is incremented in such a way as to sample the LUT to produce a waveform of the desired frequency.

## Links

- DDS
  - https://www.analog.com/en/analog-dialogue/articles/all-about-direct-digital-synthesis.html
  - https://www.fpga4fun.com/DDS.html
- Analog Circuits & Synths
  - https://www.youtube.com/watch?v=mYk8r3QlNi8&list=PLOunECWxELQS5bMdWo9VhmZtsCjhjYNcV
- Filters
  - Resonance
    - https://www.youtube.com/watch?v=YNoj9Rrw_VM&list=PPSV
  - (Moog) Ladder Filter
    - https://www.allaboutcircuits.com/technical-articles/analyzing-the-moog-filter/
- TB-303
  - Quick Start
    https://www.youtube.com/watch?v=sLT06GFIl98
  - Schematic / Service Manual
    - http://privat.bahnhof.se/wb447909/dinsync/service_manuals/TB-303.pdf
  - x0xb0x Reproduction Circuit Diagram
    - http://wiki.openmusiclabs.com/wiki/x0xb0x?action=AttachFile&do=view&target=mainboard2.png
  - Waveform Generation
    - https://www.kvraudio.com/forum/viewtopic.php?t=455469
  - VCF / Ladder Filter
    - https://www.timstinchcombe.co.uk/index.php?pge=diode1
    - https://www.timstinchcombe.co.uk/index.php?pge=diode2
  - Other
    - https://www.reddit.com/r/TechnoProduction/comments/vlfphq/303_envelope_driving_me_up_the_wall/
      https://www.kvraudio.com/forum/viewtopic.php?t=562991
    - https://www.kvraudio.com/forum/viewtopic.php?t=262829&postdays=0&postorder=asc&start=0
- Other Projects
  - [midilab/aciduino](https://github.com/midilab/aciduino/tree/master/v1/hardware)
  - [maddanio/Open303](https://github.com/maddanio/open303/tree/master/Source/DSPCode)
  - https://olawistedt.github.io/BassMatrix/
  - [gundy/tiny-synth](https://github.com/gundy/tiny-synth)
