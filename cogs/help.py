import discord
import libs.config as config
from libs.command_manager import custom_check
from discord.ext import commands

help_config = config.get_string("commands")["help"]

def extract_commands(all_commands, margin="", getcount=False):
    padding = 24 - len(margin)
    count = 0
    for command in all_commands:
        if command.hidden:
            continue
        if isinstance(command,commands.core.Group):
            _count = extract_commands(command.commands,margin=margin+"│    ", getcount=True)
            if _count > 0:
                count += 1
        else:
            count += 1

    if getcount:
        return count

    i = 0
    msg = ""
    for command in all_commands:
        if command.hidden:
            continue
        if isinstance(command,commands.core.Group):

            if i == count - 1:
                status, message = extract_commands(command.commands,margin=margin+"    ")
            else:
                status, message = extract_commands(command.commands,margin=margin+"│   ")
            if status:
                i += 1
                msg = margin
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

                msg += f"{message}\n"
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
                msg += f"{margin}"
    if i > 0:
        return (True,msg)
    return (False, "")

def get_msg(bot):
    count = 0
    for cog_name in bot.cogs:
        cog = f"\n> {cog_name}\n"
        all_commands = bot.get_cog(cog_name).get_commands()
        
        _count = extract_commands(all_commands, " │   ", getcount=True)
        if _count > 0:
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
        cog = f"\n> {cog_name}\n"

        # Loop through all commands present in cog.
        all_commands = bot.get_cog(cog_name).get_commands()
        
        if i == count -1:
            status, message = extract_commands(all_commands, margin="     ")
        else:
            status, message = extract_commands(all_commands, margin=" │   ")
        if status:
            i += 1
            if i == count:
                msg += " └── "+cog_name + "\n"
            else:
                msg += " ├── "+cog_name + "\n"
            msg += message + "\n"
    msg += "```"
    return msg

class Help(commands.Cog, name=help_config["name"]):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command(name="staff", description=s_help["staff_help"])
    # async def help_staff(self, ctx):
    #     await ctx.send(get_msg(self.bot, True))

    @commands.command(name="help", description=help_config["help"]["description"])
    @custom_check()
    async def help_user(self, ctx, *args):
        await ctx.send(get_msg(self.bot))


def setup(bot):
    bot.add_cog(Help(bot))
