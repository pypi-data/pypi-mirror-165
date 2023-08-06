# coding=utf-8
"""
[aslooper]
looper-活套
用来捕获 SIGINT, SIGTERM 信号后取消所有运行任务，
退出运行不引入asyncio报错。


[使用]
import asyncio
from aslooper import looper

# windows 系统不支持 uvloop，兼容 windows
try:
    import uvloop
except ImportError:
    class __Uvloop:
        @classmethod
        def install(cls):
            pass
    uvloop = __Uvloop


@looper
async def main():
    while True:
        print("run something.")
        await asyncio.sleep(1)

if __name__ == '__main__':
    uvloop.install()
    # Python 3.7 required
    asyncio.run(main())
"""

__version__ = "1.0.7"

__all__ = ["looper"]


import asyncio
import functools
from signal import SIGINT, SIGTERM


async def __cancel_all_tasks():
    """取消所有任务

    :return:
    """
    for task in asyncio.all_tasks():
        if task is not asyncio.current_task():
            print(f"Cancel Task {task}")
            task.cancel()


def looper(func):
    """异步函数装饰器:
    用来捕获 SIGINT, SIGTERM 信号后取消所有运行任务，退出运行不报错。
    """
    if not asyncio.iscoroutinefunction(func):
        raise TypeError(f"{func} is not coroutinefunction.")

    @functools.wraps(func)
    async def loop_signal_handler(*args, **kwargs):
        loop = asyncio.get_running_loop()
        # Add signal
        for signal in (SIGINT, SIGTERM):
            try:
                loop.add_signal_handler(
                    signal, lambda: asyncio.create_task(__cancel_all_tasks(),
                                                        name="signal_handler_call")
                )
            except NotImplementedError:
                # logger.warning(
                #     "crawler tried to use loop.add_signal_handler "
                #     "but it is not implemented on this platform."
                # )
                pass
        try:
            return await func(*args, **kwargs)
        except asyncio.CancelledError:
            print("Exit!")

    return loop_signal_handler
