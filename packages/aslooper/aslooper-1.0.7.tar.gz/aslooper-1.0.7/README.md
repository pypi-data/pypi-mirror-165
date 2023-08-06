# aslooper

> looper 
> Used to cancel all running tasks after catching SIGINT, SIGTERM signals,
> Quit running without raise asyncio error.

## 使用

```python
import asyncio
from aslooper import looper


async def run(i):
    while True:
        print(f"{i} running.")
        await asyncio.sleep(1)


@looper
async def main():
    tasks = [run(i) for i in range(3)]
    await asyncio.gather(*tasks)


asyncio.run(main())
```
