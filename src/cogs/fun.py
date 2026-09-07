import asyncio

import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sendrepo(self, ctx):
        await ctx.send("https://github.com/joshieV/discord-bot")

    @commands.command()
    #If !hello in the server is typed the bot will reply back
    async def hello(self, ctx):
        await ctx.send(f"Hello {ctx.author.mention}!")

    @commands.command()
    async def dm(self, ctx, *, msg):
        await ctx.author.send(f"Here is your message from the server -> {msg}")

    @commands.command()
    async def reply(self, ctx):
        await ctx.reply("This is the reply to your message")

    @commands.command()
    async def poll(self, ctx, *, question):
        embed = discord.Embed(title="New Poll", description=question)
        poll_message = await ctx.send(embed=embed)
        await poll_message.add_reaction("👍")
        await poll_message.add_reaction("👎")

    @commands.command()
    async def slap(self, ctx, member: discord.Member=None):
        if member is None:
            await ctx.send("Mention someone to slap them. !slap @membername")
            return

        await ctx.send(f"{member.mention} got slapped by {ctx.author.mention}!")
        await ctx.send("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDV4ZXJzMmRjNmpzZ3d4ZXNpM3dhNzZlMjlhN2g4ejg1ZHEwcGJ2YyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/mEtSQlxqBtWWA/giphy.gif")

    @commands.command()
    async def coinflip(self, ctx):
        await ctx.send("Heads or tails?")

        try:
            response = await self.bot.wait_for(
                "message",
                timeout=30.0,
                check=lambda m: m.author == ctx.author and m.channel == ctx.channel
            )

            guess = response.content.lower().strip()

            if guess not in ["heads", "tails", "h", "t"]:
                await ctx.send("Invalid choice, heads / h or tails / t")
                return

            if guess in ["heads", "h"]:
                guess = "heads"
            else:
                guess = "tails"

            flip = random.randint(0, 1)
            result = "heads" if flip == 0 else "tails"

            await ctx.send("Flipping...")
            await ctx.send("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbXVxOWEzYmw0eTJybDc0ZTg4ejY3Y2xoOGtvNmFjbGtnODRqcnJwcSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/r9JXEbkaOo12vl9P1I/giphy.gif")
            await asyncio.sleep(2)
            await ctx.send(f"Landed on {result}")

            if guess == result:
                await ctx.send("Correct")
            else:
                await ctx.send("Wrong")

        except asyncio.TimeoutError:
            await ctx.send(f"{ctx.author.mention} took too long to respond...")

    @commands.command()
    async def hug(self, ctx, member: discord.Member=None):
        if member is None:
            await ctx.send("Mention someone to hug them")
            return

        await ctx.send(f"{ctx.author.mention} hugged {member.mention}")
        await asyncio.sleep(0.5)
        await ctx.send("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcTQ4aHByeHlzc285NTYxOGIxemd4bjl3Z254YzVvYTZyODEydHZnbyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/42YlR8u9gV5Cw/giphy.gif")

async def setup(bot):
    await bot.add_cog(Fun(bot))
