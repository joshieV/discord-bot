import discord
from discord.ext import commands

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

async def setup(bot):
    await bot.add_cog(Fun(bot))
