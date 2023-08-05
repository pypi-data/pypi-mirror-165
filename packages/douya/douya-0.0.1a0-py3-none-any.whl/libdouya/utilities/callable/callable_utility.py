# -*- coding:utf-8 -*-
#!/usr/bin/env python


'''
    callable_utility.py - 可调用方法相关的通用方法集
'''

import asyncio, logging, signal, os, time
# from asyncio.tasks import wait
from typing import Any, Callable, List, Awaitable, Coroutine, Generator, AsyncGenerator, Tuple
from types import MethodType,FunctionType
from ...dataclasses.c.err import ErrorDefs,DyError

class CallableUtl:
    @staticmethod
    def is_callable(what:Any) -> bool:
        return isinstance(what, (Awaitable, Generator, AsyncGenerator, MethodType, FunctionType))

    @staticmethod
    def put_callable_deeply_until_uncallable(loop: asyncio.AbstractEventLoop, what:Any = None, *args, **kwargs):
        '''循环递归执行方法
        适用于what是一个阻塞函数
        但不适宜what里面创建一个新的事件循环并阻塞的情况(sanic)，
        '''
        def on_task_done(task: asyncio.Task):
            try:
                CallableUtl.put_callable_deeply_until_uncallable(loop, task.result(), *args, **kwargs)
            except StopAsyncIteration:
                pass
            except StopIteration:
                pass

        if not CallableUtl.is_callable(what):
            return
        elif isinstance(what, Awaitable):
            t = loop.create_task(what)
            t.add_done_callback(on_task_done)
            if not loop.is_running(): loop.run_until_complete(t)
        elif isinstance(what, Generator):
            [ CallableUtl.put_callable_deeply_until_uncallable(loop, o, *args, **kwargs) for o in what ]
        elif isinstance(what, AsyncGenerator):
            it = what.__aiter__()
            while True:
                try:
                    CallableUtl.put_callable_deeply_until_uncallable(loop, it.__anext__(), *args, **kwargs)
                except StopAsyncIteration:
                    break
        elif isinstance(what, (MethodType, FunctionType)):
            CallableUtl.put_callable_deeply_until_uncallable(loop, what(*args, **kwargs), *args, **kwargs)
        else:
            raise DyError(ErrorDefs.INVALID_ARG_FORMAT, parameter_name = "what")

    @staticmethod
    def run_callable_deeply_until_uncallable(loop: asyncio.AbstractEventLoop, what:Any = None, *args, **kwargs):
        '''循环递归执行方法
        适用于what是一个阻塞函数
        但不适宜what里面创建一个新的事件循环并阻塞的情况(sanic)，
        '''
        def on_task_done(task: asyncio.Task):
            try:
                return CallableUtl.run_callable_deeply_until_uncallable(loop, task.result(), *args, **kwargs)
            except StopAsyncIteration:
                pass
            except StopIteration:
                pass

        if what is None:
            return None
        elif isinstance(what, Awaitable):
            t = loop.create_task(what)
            t.add_done_callback(on_task_done)
            if not loop.is_running():
                loop.run_until_complete(t)
            else:
                while not t.done(): 
                    time.sleep(0.1)
        elif isinstance(what, Generator):
            [ CallableUtl.run_callable_deeply_until_uncallable(loop, o, *args, **kwargs) for o in what ]
        elif isinstance(what, AsyncGenerator):
            it = what.__aiter__()
            while True:
                try:
                    CallableUtl.run_callable_deeply_until_uncallable(loop, it.__anext__(), *args, **kwargs)
                except StopAsyncIteration:
                    break
        elif isinstance(what, (MethodType, FunctionType)):
            CallableUtl.run_callable_deeply_until_uncallable(loop, what(*args, **kwargs), *args, **kwargs)
        else:
            raise DyError(ErrorDefs.INVALID_ARG_FORMAT, parameter_name = "what")

    @staticmethod
    async def call_callable_deeply_until_uncallable(what:Any) -> Any:
        '''运行非服务的对象
        '''
        if not CallableUtl.is_callable(what):
            return what
        elif isinstance(what, Awaitable):
            return await CallableUtl.call_recursively(await what)
        elif isinstance(what, Generator):
            return [await CallableUtl.call_recursively(o) for o in what ]
        elif isinstance(what, AsyncGenerator):
            return [await CallableUtl.call_recursively(o) async for o in what ]
        elif isinstance(what, (MethodType, FunctionType)):
            return await CallableUtl.call_recursively(what())
        else:
            raise DyError(ErrorDefs.INVALID_ARG_FORMAT, parameter_name = "what")

    @staticmethod
    async def call_callable_deeply_until_uncallable_later(delay:int, what:Any) -> Any:
        await asyncio.sleep(delay, asyncio.get_running_loop())
        return await CallableUtl.call_callable_deeply_until_uncallable(delay, what)

    # def call_thing_forever(loop: asyncio.AbstractEventLoop, what:Any, cond: Callable):
    #     '''利用run_forever执行任务
    #     如果满足条件，则使用run_forever启动事件循环，阻塞在此处。直到事件循环退出。
    #     如果不满足条件，则递归调用call_serve直到任务结束。

    #     调用则可以通过返回一个阻塞的内部函数，来达到阻塞自定义的要求。
    #     '''
    #     def recur(v): return loop.run_forever() if cond(v) else call_thing_forever(loop, v, recur)

    #     if is_callable(what): call_thing(loop = loop, what = what, callback = recur)