import asyncio
import inspect
import random
import time
import aiohttp
import requests
from pprint import pprint

POKEMON_URL = f'https://pokeapi.co/api/v2/pokemon/'
TESTING = False
PRINT_RESULT = False
NUM_OF_POKEMON = 10 if TESTING else 100


def timer(name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            s = time.time()
            res = func(*args, **kwargs)
            print(f'{name}: Time took {time.time() - s}')

            return res
        return wrapper
    return decorator


def get_url():
    return f'{POKEMON_URL}{random.randint(1, 151)}'


class Pokemon:
    def get_pokemon(self):
        if TESTING:
            time.sleep(1)
            return {'name': 'abc'}
        else:
            return requests.get(get_url()).json()


class AsyncPokemon(Pokemon):
    async def get_pokemon(self):
        if TESTING:
            await asyncio.sleep(1)
            return {'name': 'abc'}
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(get_url()) as resp:
                    return await resp.json()


async def _run_async():
    return await AsyncPokemon().get_pokemon()


async def main():
    tasks = [_run_async() for _ in range(NUM_OF_POKEMON)]
    return await asyncio.gather(*tasks)


@timer('Async')
def run_async():
    result = asyncio.run(main())
    if PRINT_RESULT:
        pprint([r['name'] for r in result])


@timer('Sync')
def run_sync():
    p = Pokemon()
    result = [p.get_pokemon() for _ in range(NUM_OF_POKEMON)]
    if PRINT_RESULT:
        pprint([r['name'] for r in result])


if __name__ == '__main__':
    print(f'Running: Num of Pokemon {NUM_OF_POKEMON} (Testing {TESTING})')
    run_sync()
    run_async()
    print(inspect.iscoroutinefunction(Pokemon().get_pokemon))
    print(inspect.iscoroutinefunction(AsyncPokemon().get_pokemon))
