import asyncio

def async_to_sync(awaitable, loop=None, complete=False):
    from functions.opheliaDiscord import discordLoop
    if loop is None: 
        loop = discordLoop
    try:
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(awaitable, loop)
            return future.result() if complete else future
        else: 
            print("Loop is not running")
            return loop.run_until_complete(awaitable)
    except Exception as e: print(f"Error in async to sync: {e}")


def async_to_sync_params(awaitable, loop, complete=False, *args, **kwargs):
    try:
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(awaitable(*args, **kwargs), loop)
            return future.result() if complete else future
        else: 
            print("Loop is not running")
            return loop.run_until_complete(awaitable(*args, **kwargs))
    except Exception as e: print(f"Error in async to sync with params: {e}")