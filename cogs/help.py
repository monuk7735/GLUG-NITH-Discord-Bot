import discord
from discord.ext import commands
from discord.ext.commands import Context

import libs.config as config
from libs.command_manager import custom_check

help_config = config.get_string("commands")["help"]

mod_roles = config.get_config("roles")["mod"]


def get_count(all_commands, is_mod=False):
    count = 0
    for command in all_commands:
        if command.hidden and not is_mod:
            continue
        if isinstance(command, commands.core.Group):
            if get_count(command.commands, is_mod=is_mod) > 0:
                count += 1
        else:
            count += 1
    return count


def extract_commands(all_commands, margin="", is_mod=False):
    padding = 24 - len(margin)

    count = get_count(all_commands, is_mod=is_mod)

    i = 0
    msg = ""
    for command in all_commands:
        if command.hidden and not is_mod:
            continue
        if isinstance(command, commands.core.Group):
            if i == count - 1:
                status, message = extract_commands(
                    command.commands, margin=margin+"    ", is_mod=is_mod)
            else:
                status, message = extract_commands(
                    command.commands, margin=margin+"│   ", is_mod=is_mod)
            if status:
                i += 1
                msg += margin
                if i == count:
                    msg += "└── "
                else:
                    msg += "├── "
                tmp = command.name
                if command.usage:
                    tmp += f" {command.usage}"
                msg += f"{tmp:{padding}s}"
                if command.description:
                    msg += f" │ {command.description}"

                msg += f"\n{message}"
        else:
            i += 1
            msg += margin
            if i == count:
                msg += "└── "
            else:
                msg += "├── "
            tmp = command.name
            if command.usage:
                tmp += f" {command.usage}"
            msg += f"{tmp:{padding}s}"
            if command.description:
                msg += f" │ {command.description}"
            msg += "\n"
            if i == count:
                msg += f"{margin}\n"
    if i > 0:
        return (True, msg)
    return (False, "")


def get_msg(bot, is_mod):
    count = 0
    for cog_name in bot.cogs:

        all_commands = bot.get_cog(cog_name).get_commands()

        if get_count(all_commands, is_mod=is_mod) > 0:
            count += 1

    msg = f"```\n"
    msg += f"{' '*6}   _|_|_|  _|        _|    _|    _|_|_| \n"
    msg += f"{' '*6} _|        _|        _|    _|  _|       \n"
    msg += f"{' '*6} _|  _|_|  _|        _|    _|  _|  _|_| \n"
    msg += f"{' '*6} _|    _|  _|        _|    _|  _|    _| \n"
    msg += f"{' '*6}   _|_|_|  _|_|_|_|    _|_|      _|_|_| \n"

    msg += "\n"
    msg += "          {required args} [optional args]\n"
    msg += "\n"
    msg += "\n"
    msg += "glug\n"
    msg += " │\n"

    i = 0
    for cog_name in bot.cogs:

        # Loop through all commands present in cog.
        all_commands = bot.get_cog(cog_name).get_commands()

        if i == count - 1:
            status, message = extract_commands(
                all_commands, margin="     ", is_mod=is_mod,)
        else:
            status, message = extract_commands(
                all_commands, margin=" │   ", is_mod=is_mod,)
        if status:
            i += 1
            if i == count:
                msg += " └── "+cog_name + "\n"
            else:
                msg += " ├── "+cog_name + "\n"
            msg += message
    msg += "```"
    return msg


class Help(commands.Cog, name=help_config["name"]):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command(name="staff", description=s_help["staff_help"])
    # async def help_staff(self, ctx:Context):
    #     await ctx.send(get_msg(self.bot, True))

    @commands.command(name="help", description=help_config["help"]["description"])
    @custom_check()
    async def help_user(self, ctx:Context, *args):
        await ctx.send(get_msg(self.bot, False))

    @commands.command(name="mod", description=help_config["help"]["description"], hidden=True)
    @custom_check(req_roles=mod_roles)
    async def help_mod(self, ctx:Context, *args):
        await ctx.send(get_msg(self.bot, True))


def setup(bot):
    bot.add_cog(Help(bot))
