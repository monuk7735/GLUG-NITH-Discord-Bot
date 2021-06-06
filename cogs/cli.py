import discord
from discord.ext import commands
from discord.ext.commands import Context

import libs.config as config
from libs.command_manager import custom_check, extract_member_id

cli_config = config.get_string("commands")["cli"]

"""
Args:
    users: List of discord.member
    args: args passed to the command function after the context variable

Returns:
    msg: String with role IDs of given users
"""


def get_user_ids(users, args):
    msg = "```"
    for i, user in enumerate(users):
        msg += "\n\n"
        if not user:
            msg += f"{args[i]}: no such member"
            continue

        msg += f"uid={user.id}({user.name}) "
        msg += f"gid={user.guild.id}({user.guild.name}) "
        msg += "roles="

        for role in user.roles:
            msg += f"{role.id}({role.name}),"

        msg = msg[:-1]
    msg += "\n```"
    return msg


class Cli(commands.Cog, name=cli_config["name"]):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="echo", description=cli_config["echo"]["description"], usage=cli_config["echo"]["usage"])
    @custom_check()
    async def echo(self, ctx:Context, *args):
        await ctx.channel.send(f'```\n{" ".join(args)} \n```')

    @commands.command(name="id", description=cli_config["id"]["description"], usage=cli_config["id"]["usage"])
    @custom_check(allowed_in_dm=False)
    async def id(self, ctx:Context, *args):
        users: list = []
        if len(args) == 0:
            users = [ctx.author]
        else:
            for user_id in args:
                user = ctx.guild.get_member(extract_member_id(user_id))
                users.append(user)
        msg = get_user_ids(users, args)

        await ctx.channel.send(msg)

    @commands.command(name="root", description=cli_config["root"]["description"])
    @custom_check(allowed_in_dm=False)
    async def owner(self, ctx:Context):
        await ctx.channel.send(f"```\nThe server owner is {ctx.author.guild.owner.name}\n```")


def setup(bot):
    bot.add_cog(Cli(bot))
