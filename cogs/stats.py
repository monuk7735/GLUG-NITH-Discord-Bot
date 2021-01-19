import discord
from discord.ext import commands

import libs.config as config
from libs.command_manager import custom_check

stats_config = config.get_string("commands")["stats"]

"""
Args:
    ctx: Context object

Returns:
    msg: String with member count
"""


async def get_count(ctx):
    msg = "```\n"
    bot_count = 0
    human_count = 0
    for member in ctx.author.guild.members:
        if member.bot:
            bot_count += 1
        else:
            human_count += 1
    msg += f"Total Members : {ctx.author.guild.member_count}\n"
    msg += f"Bots          : {bot_count}\n"
    msg += "\n```"
    return msg


class Stats(commands.Cog, name=stats_config["name"]):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stats", description=stats_config["stats"]["description"], usage=stats_config["stats"]["usage"],hidden=True)
    @custom_check(allowed_in_dm=False)
    async def id(self, ctx):
        msg = await get_count(ctx)
        await ctx.channel.send(msg)


def setup(bot):
    bot.add_cog(Stats(bot))
