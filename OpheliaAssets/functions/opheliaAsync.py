import asyncio

def async_to_sync(awaitable, loop=None, complete=False):
    """
        Use this function to await a coroutine in a separate thread. Mainly to use async functions from a sync method. Will return the result if complete=True, otherwise will return the future. Will fail and return if the loop is not running
    """
    from functions.opheliaDiscord import discordLoop
    if loop is None: 
        loop = discordLoop
    try:
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(awaitable, loop)
            return future.result() if complete else future
        else: 
            return("Loop is not running")
    except Exception as e: print(f"Error in async to sync: {e}")

def async_to_sync_params(awaitable, loop, complete=False, *args, **kwargs):
    """
        Admittedly, useless. Just use async_to_sync.
    """
    try:
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(awaitable(*args, **kwargs), loop)
            return future.result() if complete else future
        else: 
            return("Loop is not running")
    except Exception as e: print(f"Error in async to sync with params: {e}")