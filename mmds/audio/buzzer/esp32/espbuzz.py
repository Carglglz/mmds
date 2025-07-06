from machine import PWM, Pin
import asyncio
import time


class AsyncBuzzer:
    def __init__(self, pin, timer=2, freq=440, duty=512):
        self.buzz = PWM(Pin(pin), freq=freq, duty=duty)
        self.buzz.deinit()
        # self.buz_tim = Timer(timer)

    def play(self, freq, msec):
        if freq > 0:
            self.buzz.init()
            self.buzz.freq(freq)
            time.sleep_ms(msec)
            self.buzz.deinit()

    def buzz_beep(self, sleeptime, ntimes, ntimespaced, fq):
        for i in range(ntimes):
            self.play(fq, sleeptime)
            time.sleep_ms(ntimespaced)

    async def aplay(self, freq, msec):
        if freq > 0:
            self.buzz.init()
            self.buzz.freq(freq)
            await asyncio.sleep_ms(msec)
            self.buzz.deinit()

    async def abuzz_beep(self, sleeptime, ntimes, ntimespaced, fq):
        for i in range(ntimes):
            await self.play(fq, sleeptime)
            await asyncio.sleep_ms(ntimespaced)

    async def warning(self, fl=4000, fh=800, ts=100, ntimes=10):
        for i in range(ntimes):
            await self.play(fl, ts)
            await self.play(fh, ts)

    async def error(self, fq=100):
        await self.buzz_beep(350, 2, 50, fq)
