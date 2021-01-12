import discord
from discord.ext import commands

from libs.command_manager import custom_check
from libs.embed  import officialEmbed


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="embed", description="Display an embed", usage="{Title} {Desc}", hidden=True)
    @custom_check()
    async def echo(self, ctx, title, *args):
        embed = officialEmbed(title, " ".join(args))
        await ctx.channel.send(embed=embed)

    

def setup(bot):
    bot.add_cog(Test(bot))
