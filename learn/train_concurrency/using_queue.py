import asyncio, time, random, os
import itertools as it


async def makeitem(size: int = 5) -> str:
    return os.urandom(size).hex()


async def randsleep(caller = None) -> None:
    i = random.randint(0, 10)
    if caller:
        print(f"{caller} sleeping for {i} seconds")
    await asyncio.sleep(i)


async def produce(name: int, q: asyncio.Queue) -> None:
    n = random.randint(0, 10)
    for _ in it.repeat(None, n):
        await randsleep(caller=f"Producer {name}")
        i = await makeitem()
        t = time.perf_counter()
        await q.put((i, t))
        print(f"Producer {name} added {i} to queue")


async def consume(name: int, q: asyncio.Queue) -> None:
    while True:
        await randsleep(caller=f"Consumer {name}")
        i, t = await q.get()
        now = time.perf_counter()
        print(f"Consumer {name} get element {i} in {now - t:0.5f} seconds")
        q.task_done()


async def main(nprod: int, ncon: int):
    q = asyncio.Queue()
    producers = [asyncio.create_task(produce(n, q)) for n in range(nprod)]
    consumers = [asyncio.create_task(consume(n, q)) for n in range(ncon)]
    await asyncio.gather(*producers)
    await q.join() # Implicitly await consumers
    for c in consumers:
        c.cancel()


if __name__ == "__main__":
    random.seed(time.time())
    start = time.perf_counter()
    asyncio.run(main(2, 6))
    elapsed = time.perf_counter() - start
    print(f"Finished in {elapsed:.3f} seconds")