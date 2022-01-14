import time
import asyncio
import random


color = (
    "\033[0m",   # End of color
    "\033[36m",  # Cyan
    "\033[91m",  # Red
    "\033[35m",  # Magenta
)


async def makerandom(idx: int, threshold: int = 6) -> int:
    print(color[idx + 1] + f"Init makerandom({idx})")
    i = random.randint(0, 10)
    while i <= threshold:
        print(color[idx+1] + f"makerandom({idx}) == {i} too low; retrying")
        await asyncio.sleep(idx + 1)
        i = random.randint(0, 10)
    print(color[idx + 1] + f"Finished: makerandom({idx}) == {i}" + color[0])
    return i


async def main():
    res = await asyncio.gather(*(makerandom(i, 10 - i - 1) for i in range(3)))
    return res


if __name__ == "__main__":
    random.seed(time.time())
    r1, r2, r3 = asyncio.run(main())
    print(f"\nr1: {r1}\nr2: {r2}\nr3: {r3}")
