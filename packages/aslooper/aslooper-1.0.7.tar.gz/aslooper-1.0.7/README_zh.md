# aslooper

> looper(活套)
> 用来捕获 SIGINT, SIGTERM 信号后取消所有运行任务，
> 退出运行不引入asyncio报错。

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
