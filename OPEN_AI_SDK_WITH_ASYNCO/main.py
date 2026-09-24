import asyncio


async def mul ():
    await asyncio.sleep(10)
    print("This is mul function")
async def add():
    await asyncio.sleep(5)
    print("This is add function")
async def sub():
    print("This is sunstruct fucntion")
async def main():
    await asyncio.gather(add(), mul(), sub())





if __name__ == "__main__":
    asyncio.run(main())
    

