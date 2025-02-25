import asyncio

def async_to_sync(awaitable, loop):
    try:
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(awaitable, loop)
            return future
        else: 
            print("Loop is not running")
            return loop.run_until_complete(awaitable)
    except Exception as e: print(e)

def async_to_sync_params(awaitable, loop, *args, **kwargs):
    try:
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(awaitable(*args, **kwargs), loop)
            return future
        else: 
            print("Loop is not running")
            return loop.run_until_complete(awaitable(*args, **kwargs))
    except Exception as e: print(e)