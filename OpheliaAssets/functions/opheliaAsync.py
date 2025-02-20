import asyncio

def async_to_sync(awaitable, loop):
    try:
        if loop.is_running():
            return asyncio.run_coroutine_threadsafe(awaitable, loop).result()
        else: 
            print("Loop is not running")
            return loop.run_until_complete(awaitable)
    except: pass