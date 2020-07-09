#!/usr/bin/env python3
# countasync.py

import asyncio

async def count(sl):
    print("One",sl)
    await asyncio.sleep(sl)
    print("Two",sl)

async def main():
    await asyncio.gather(count(5), count(2), count(1))

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
