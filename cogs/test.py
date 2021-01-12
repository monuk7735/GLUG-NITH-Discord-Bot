import discord
from discord.ext import commands

from libs.command_manager import check_is_activated
from libs.embed  import officialEmbed


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="embed", description="Display an embed", usage="{Title} {Desc}")
    @check_is_activated()
    async def echo(self, ctx, title, *args):
        embed = officialEmbed(title, " ".join(args))
        await ctx.channel.send(embed=embed)

    

def setup(bot):
    bot.add_cog(Test(bot))
