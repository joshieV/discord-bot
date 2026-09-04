import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

_role = "test_subject"

@bot.event
async def on_ready():
    print(f"Test {bot.user.name}")

@bot.event
async def on_member_join(member):
    # DMs the user a welcome message when they join the server
    await member.send(f"Welcome {member.name} to the server!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "fudge" in message.content.lower():
        #Deletes the bad word and replies
        await message.delete()
        await message.channel.send(f"{message.author.mention} No bad words please!")

    await bot.process_commands(message)

@bot.command()
#If !hello in the server is typed the bot will reply back
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
#Function for assigning a test role for now
async def assignrole(ctx):
    role = discord.utils.get(ctx.guild.roles, name=_role)

    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} now has {_role} role")
    else:
        await ctx.send("This role does not exist!")

@bot.command()
async def removerole(ctx):
    role = discord.utils.get(ctx.guild.roles, name=_role)

    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} no longer has the {_role} role")
    else:
        await ctx.send("This role does not exist!")

@bot.command()
@commands.has_role(_role)
async def secret(ctx):
    await ctx.send("Welcome you test monkey")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You dont have permission")

@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"Here is your message from the server -> {msg}")

@bot.command()
async def reply(ctx):
    await ctx.reply("This is the reply to your message")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)

