import discord
from discord.ext import commands

_role = "test_subject"

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # DMs the user a welcome message when they join the server
        await member.send(f"Welcome {member.name} to the server!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if "fudge" in message.content.lower():
            #Deletes the bad word and replies
            await message.delete()
            await message.channel.send(f"{message.author.mention} No bad words please!")

    @commands.command()
    #Function for assigning a test role for now
    async def assignrole(self, ctx):
        role = discord.utils.get(ctx.guild.roles, name=_role)

        if role:
            await ctx.author.add_roles(role)
            await ctx.send(f"{ctx.author.mention} now has {_role} role")
        else:
            await ctx.send("This role does not exist!")

    @commands.command()
    async def removerole(self, ctx):
        role = discord.utils.get(ctx.guild.roles, name=_role)

        if role:
            await ctx.author.remove_roles(role)
            await ctx.send(f"{ctx.author.mention} no longer has the {_role} role")
        else:
            await ctx.send("This role does not exist!")

    @commands.command()
    @commands.has_role(_role)
    async def secret(self, ctx):
        await ctx.send("Welcome you test monkey")

    @secret.error
    async def secret_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("You dont have permission")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
