import time, random, asyncio


async def part_1(n: int) -> str:
    i = random.randint(0, 10)
    print(f"part_1 sleeping for {i} seconds")
    await asyncio.sleep(i)
    result = f"result{n}-1"
    print(f"Returning part_1({n}) == {result}")
    return result


async def part_2(n: int, arg: str) -> str:
    i = random.randint(0, 10)
    print(f"part_2 sleeping for {i} seconds")
    await asyncio.sleep(i)
    result = f"result{n}-2 derived from {arg}"
    print(f"Returning part_2({n, arg}) == {result}")
    return result


async def chain(n: int) -> None:
    t1 = time.perf_counter()
    p1 = await part_1(n)
    p2 = await part_2(n, p1)
    t2 = time.perf_counter() - t1
    print(f"Chained result{n} => {p2} (took {t2:.3f} seconds)")


async def main(*args):
    await asyncio.gather(*(chain(n) for n in args))


# Call main
input_value = [5, 8, 12]
start = time.perf_counter()
asyncio.run(main(*input_value))
elapsed = time.perf_counter() - start
print(f"Finished in {elapsed:.3f} seconds")