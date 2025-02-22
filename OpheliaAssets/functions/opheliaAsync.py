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