import aiohttp
import asyncio
import random


params = {"text": "foo", "batt": 20, "wifi": -20, "temp": 20}


async def main():
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get("http://0.0.0.0:8181/", params=params) as response:
                html = await response.text()
                print(html, response.status)
            await asyncio.sleep(5)
            params.update(
                text=html,
                batt=random.randint(0, 100),
                wifi=random.randint(-80, -20),
                temp=random.randint(15, 30),
            )
            print(params)


asyncio.run(main())
