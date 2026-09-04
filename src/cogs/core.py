from discord.ext import commands

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Test {self.bot.user.name}")

async def setup(bot):
    await bot.add_cog(Core(bot))
