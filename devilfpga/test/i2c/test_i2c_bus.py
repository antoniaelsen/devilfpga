from amaranth.sim import Simulator
from ...i2c.i2c_bus import I2CBus


# def test_i2c_bus():
#     dut = I2CBus()
#     sim = Simulator(dut)
#     sim.add_clock(1 / (48000 * 256))

#     def bench():
#         yield dut.mclk.eq(0)
#         yield dut.lrclk.eq(0)
#         yield dut.o_audio.eq(0)
#         yield
#         assert (yield dut.o_audio) == 0

#         yield dut.mclk.eq(1)

#         for _ in range(64):  # 16 * 2 * 2 clk cycles per sample
#             yield dut.aud_adc.eq(0xABCD)
#             yield

#             if (yield dut.lrclk):
#                 # Right channel
#                 assert (yield dut.o_audio) == 0xABCD
#             else:
#                 # Left channel
#                 assert (yield dut.o_audio) == 0xABCD

#     sim.add_sync_process(bench)
#     with sim.write_vcd("test_i2c_bus.vcd"):
#         sim.run()
