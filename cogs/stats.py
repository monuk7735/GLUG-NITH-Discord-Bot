import discord
from discord.ext import commands

import libs.config as config
from libs.command_manager import custom_check, get_role

stats_config = config.get_string("commands")["stats"]
optional_roles = config.get_config("roles")["optional"]

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
    msg += f"{'Total Members':20s}: {ctx.author.guild.member_count}\n\n"

    msg += f"{'Humans':20s}: {ctx.author.guild.member_count-bot_count}\n"
    msg += f"{'Bots':20s}: {bot_count}\n\n"

    for role_id in optional_roles:
        role = get_role(ctx, role_id)
        if role:
            msg += f"{role.name:20s}: {len(role.members)}\n"

    msg += "\n```"
    return msg


class Stats(commands.Cog, name=stats_config["name"]):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stats", description=stats_config["stats"]["description"], usage=stats_config["stats"]["usage"], hidden=True)
    @custom_check(allowed_in_dm=False)
    async def id(self, ctx):
        msg = await get_count(ctx)
        await ctx.channel.send(msg)


def setup(bot):
    bot.add_cog(Stats(bot))
