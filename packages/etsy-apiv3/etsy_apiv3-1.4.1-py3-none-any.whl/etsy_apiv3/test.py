import asyncio


async def test(i):
    return i

async def create_tasks():
    tasks = []
    for i in range(20):
        tasks.append(asyncio.create_task(test(i)))
        
    result = await asyncio.gather(*tasks)
    return result

result = asyncio.run(create_tasks())
