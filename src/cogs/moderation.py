from json import JSONDecodeError

import discord
from discord.ext import commands
import json
from pathlib import Path

_role = "test_subject"

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.filtered_words = self.get_filtered_words()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # DMs the user a welcome message when they join the server
        await member.send(f"Welcome {member.name} to the server!")

    def get_filtered_words(self):
        words_file = Path(__file__).resolve().parent.parent / "data" / "bad_words.json"
        try:
            with open(words_file, "r") as f:
                data = json.load(f)
                return data.get("bad_words", [])
        except FileNotFoundError as e:
            print(f"File not found {e}")
            return []
        except JSONDecodeError as e:
            print(f"Invalid JSON file {e}")
            return []

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        content_lower = message.content.lower()

        for word in self.filtered_words:
            if word.lower() in content_lower:
                # Raises forbidden if the bot lacks Manage Messages, or in a DM
                try:
                    await message.delete()
                    await message.channel.send(f"{message.author.mention} No bad words please!")
                except discord.Forbidden as e:
                    print(e)
                break

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            if member.guild.system_channel:
                await member.guild.system_channel.send(f"Goodbye {member.display_name}")
        except discord.Forbidden:
            print(f"Missing permissions to send goodbye message in {member.guild.name}")
        except discord.HTTPException as e:
            print(f"Failed to send goodbye message in {member.guild.name}: {e}")
        except AttributeError:
            print(f"Guild or system channel not found for {member}")

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
