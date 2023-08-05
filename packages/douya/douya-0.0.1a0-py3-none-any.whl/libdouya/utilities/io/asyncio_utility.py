# -*- coding:utf-8 -*-
#!/usr/bin/env python


'''
    async_utility.py - 异步相关的通用方法集
'''

import asyncio, logging, signal, os, time
from typing import Callable

class AsyncioUtl(object):
    @staticmethod
    def cancel_all_event_loop_tasks(loop: asyncio.AbstractEventLoop) -> None:
        tasks = [task for task in asyncio.all_tasks(loop) if not task.done()]
        if not tasks:
            return

        for task in tasks:
            task.cancel()

        loop.run_until_complete(asyncio.gather(*tasks, loop=loop, return_exceptions=True))

        for task in tasks:
            if not task.cancelled() and task.exception() is not None:
                loop.call_exception_handler(
                    {
                        "message": "unhandled exception during shutdown",
                        "exception": task.exception(),
                        "task": task,
                    }
                ) 

    @staticmethod
    def set_signal_handler_for_event_loop(loop: asyncio.AbstractEventLoop, handler:Callable = None):
        def handle_sig(signum, frame):
            logging.info(f"Capture signal: {signal.Signals(signum).name}")
            if handler is not None: handler(loop, signum, frame)
            if loop.is_running(): loop.stop()

        if 'posix' == os.name:
            signal.signal(signal.SIGINT, handle_sig)
            signal.signal(signal.SIGTERM, handle_sig)

    # @staticmethod
    # def run_forever_until_close(loop: asyncio.AbstractEventLoop, what:Any, transform: Callable[[Any],Any] = None):
    #     try:
    #         if what is not None: loop.create_task(call_recursively(what, transform))
    #         loop.run_forever()
    #     except:
    #         logging.exception("Failed to call run forever")
    #     finally:
    #         # loop.run_until_complete(loop.shutdown_asyncgens())
    #         tasks = [task for task in asyncio.all_tasks(loop) if not task.done()]
    #         if tasks: loop.run_until_complete(asyncio.gather(*tasks, loop = loop, return_exceptions = True))
    #         loop.close()

    