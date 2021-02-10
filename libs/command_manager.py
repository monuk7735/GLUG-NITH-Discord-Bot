import functools

from discord.ext import commands
import discord

import libs.config as config
from libs.embed import officialEmbed

"""
Any and all checks common to more than one command should be performed here
"""

"""Decorator for any checks.

    Wrap around a bot command to check appropriate permission and channel context of the executed command from
    the Context object provided by the bot's event listener method, and errors out if checks do not pass.

    Example Usage:
        @commands.command...
        @custom_check(allowed_channels= ['channel-name1'], dm_flag= True)
        def echo...

    Args:
        allowed_channels = List of allowed channels.
        allowed_in_dm = Whether a command is allowed in DM or not,  defaults to True

    Returns:
        A Decorator to check for given conditions
    """


def custom_check(allowed_channels=[], allowed_in_dm=True):
    
    def guild_check(cmd):

        @functools.wraps(cmd)
        async def wrapper(*args, **kwargs):
            ctx = args[1]
            print(f"{ctx.author}({ctx.author.id}) in {ctx.channel.name}({ctx.author.guild.name}): {ctx.message.content}")
            if type(ctx) is not commands.Context:
                print("ERROR: Missing ctx variable in @custom_check() call in",
                      cmd.__name__, " command!")
                raise commands.MissingRequiredArgument(ctx)
            if isinstance(ctx.channel, discord.channel.DMChannel):
                if not allowed_in_dm:
                    await ctx.channel.send("Command not allowed in DM")
                    return False
            else:
                if len(allowed_channels) > 0:
                    if not ctx.channel.name in allowed_channels + ['glug-bot-test']:
                        print(
                            f"Command used in {ctx.channel.name} channel while allowed channels were {str(allowed_channels)}")
                        return False
                else:
                    if not ctx.channel.name in ['bot-commands', 'bot-testing', 'glug-bot-test']:
                        print(f"Command used in {ctx.channel.name}")
                        return False

            return await cmd(*args, **kwargs)

        return wrapper

    return guild_check


"""
Function to get Member object from user_id

Args:
    ctx: The context passed to the command function
    user_id: The mentioned user_id

Returns:
    member: Member if found otherwise None
"""


def get_member(ctx, user_id):
    try:
        if '<@!' in user_id:
            user = ctx.author.guild.get_member(int(user_id[3:-1]))
        elif '<@' in user_id:
            user = ctx.author.guild.get_member(int(user_id[2:-1]))
        else:
            user = ctx.author.guild.get_member(int(user_id))
    except ValueError:
        user = None

    return user


"""
Function to get Role object from role_id

Args:
    ctx: The context passed to the command function
    role_id: The mentioned role_id

Returns:
    role: Role if found otherwise None
"""


def get_role(ctx, role_id):
    try:
        if '<@&' in role_id:
            role = ctx.author.guild.get_role(int(role_id[3:-1]))
        elif '<@' in role_id:
            role = ctx.author.guild.get_role(int(role_id[2:-1]))
        else:
            role = ctx.author.guild.get_role(int(role_id))
    except ValueError:
        role = None

    return role


"""
Function to send contribution embed as reply

Args:
    ctx: context variable which is passed to a command function

Returns:
    None
"""


async def contribute(ctx):
    embed = officialEmbed(
        "Contribute", "Contribute to this project, help create more cool features", url=config.get_config("info")["url"])
    embed.set_thumbnail(url=config.get_string("logos")["github"])
    await ctx.send(embed=embed)
