import discord
from discord.ext import commands, tasks

import aiohttp
import datetime
from zoneinfo import ZoneInfo
import os


class DailyLeetCode(commands.Cog):
    def __init__(self, bot, channel_id):
        self.bot = bot
        self.channel_id = channel_id
        self.daily_loop.start()

    async def fetch_daily_problem(self):
        url = "https://leetcode.com/graphql"
        query = """
        query questionOfToday {
            activeDailyCodingChallengeQuestion {
                question {
                    questionFrontendId
                    title
                    titleSlug
                    difficulty
                }
            }
        }
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={'query': query}) as resp:
                resp.raise_for_status()
                data = await resp.json()

        q = data['data']['activeDailyCodingChallengeQuestion']['question']
        return {
            'id': q['questionFrontendId'],
            'title': q['title'],
            'difficulty': q['difficulty'],
            'url': f"https://leetcode.com/problems/{q['titleSlug']}/",
        }

    def build_embed(self, problem):
        colors = {
            'Easy': discord.Color.green(),
            'Medium': discord.Color.gold(),
            'Hard': discord.Color.red(),
        }
        return discord.Embed(
            title=f"{problem['id']}. {problem['title']}",
            url=problem['url'],
            description=f"**Difficulty:** {problem['difficulty']}",
            color=colors.get(problem['difficulty'], discord.Color.blue()),
        )

    @tasks.loop(time=datetime.time(hour=9, minute=0, tzinfo=ZoneInfo("Europe/London")))
    async def daily_loop(self):
        channel = self.bot.get_channel(self.channel_id)
        if channel is None:
            print(f"LeetCode channel {self.channel_id} not found")
            return

        try:
            problem = await self.fetch_daily_problem()
        except Exception as e:
            await channel.send(f"Couldn't fetch today's problem: `{e}`")
            return

        await channel.send(embed=self.build_embed(problem))

    @commands.command()
    async def leetcode(self, ctx):
        try:
            problem = await self.fetch_daily_problem()
        except Exception as e:
            await ctx.send(f"Fetch failed: `{e}`")
            return

        await ctx.send(embed=self.build_embed(problem))

async def setup(bot):
    raw = os.getenv("LEETCODE_CHANNEL_ID")

    if not raw:
        raise RuntimeError("LEETCODE_CHANNEL_ID is not in .env")
    channel_id = int(raw)
    await bot.add_cog(DailyLeetCode(bot, channel_id))