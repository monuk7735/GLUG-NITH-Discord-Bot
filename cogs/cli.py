import discord
from discord.ext import commands

import libs.config as config
from libs.command_manager import check_is_activated

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
        if user is None:
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


class Cli(commands.Cog, name="Commands to emulate CLI"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="echo", description=config.get_string("description")['cli']['echo'], usage="[string]")
    @check_is_activated()
    async def echo(self, ctx, *args):
        await ctx.channel.send(f'```{" ".join(args)} ```')

    @commands.command(name="whoami", description=config.get_string("description")['cli']['whoami'])
    @check_is_activated()
    async def whoami(self, ctx):
        await ctx.channel.send(f"```{ctx.author.name}```")

    @commands.command(name="id", description=config.get_string("description")['cli']['id'], usage="[@mention]")
    @check_is_activated()
    async def id(self, ctx, *args):
        users: list = []
        if len(args) == 0:
            users = [ctx.author]
        else:
            for user_id in args:
                try:
                    if '<@!' in user_id:
                        user = ctx.author.guild.get_member(int(user_id[3:-1]))
                    elif '<@' in user_id:
                        user = ctx.author.guild.get_member(int(user_id[2:-1]))
                    else:
                        user = None
                    users.append(user)
                except ValueError:
                    users.append(None)

        msg = get_user_ids(users, args)
        
        await ctx.channel.send(msg)

    @commands.command(name="root", description=config.get_string("description")['cli']['root'])
    @check_is_activated()
    async def owner(self, ctx):
        await ctx.channel.send(f"This server was created by {ctx.author.guild.owner.name}")


def setup(bot):
    bot.add_cog(Cli(bot))
