from __future__ import annotations

from ._client import DisClient
from aiohttp import ClientSession
from .errors import NotVoted
from discord import Member


async def is_voted(bot, topgg_token: str, user: Member):
    async with ClientSession() as cs:
            async with cs.get(
                url=f'https://top.gg/api/bots/{bot.user.id}/check',
                params={
                    "userId": user.id,
                }, 
                headers={
                    "Authorization": topgg_token
                }
            ) as ret:
                try:
                    data = await ret.json()
                    print(data)
                except:
                    return True
                if ret.status != 200:
                    return True
                
                return (data["voted"])