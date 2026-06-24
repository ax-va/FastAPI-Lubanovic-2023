import asyncio


async def q():
    print("Why can't programmers tell jokes?")
    await asyncio.sleep(3)


async def a():
    print("Timing!")


async def main():
    await asyncio.gather(q(), a())


if __name__ == "__main__":
    asyncio.run(main())
