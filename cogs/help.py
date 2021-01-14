import discord
import libs.config as config
from libs.command_manager import custom_check
from discord.ext import commands

def get_msg(bot):

    """Fabricates the output message by loading COGs and commands informations."""

    msg = f"```markdown\n"
                                                                 
    msg += f"{' '*6}_|      _|  _|_|_|  _|_|_|_|_|  _|    _| \n"
    msg += f"{' '*6}_|_|    _|    _|        _|      _|    _| \n"
    msg += f"{' '*6}_|  _|  _|    _|        _|      _|_|_|_| \n"
    msg += f"{' '*6}_|    _|_|    _|        _|      _|    _| \n"
    msg += f"{' '*6}_|      _|  _|_|_|      _|      _|    _| \n"
 
    msg += "\n         {required args} [optional args]\n"
    msg += "\n"

    # msg = f"```markdown\n"

    # Loops through cogs.
    for cog_name in bot.cogs:
        cog = f"\n> {cog_name}\n"

        # Command number
        i = 0

        # Loop through all commands present in cog.
        commands = bot.get_cog(cog_name).get_commands()
        for command in commands:
            if command.hidden:
                continue
            i = i+1
            name = command.name

            # Display only stuff that exists.
            if not command.usage == None:
                name +=  f" {command.usage}"
            
            cog += f"{name:22s}"

            if not command.description == "":
                cog +=  f" | {command.description}"
                
            cog += "\n"

        # If all commands in cog are hidden, don't print its name.
        if i > 0:
            msg += cog

    msg += "```"
    return msg

class Help(commands.Cog, name=config.get_string("description")["help"]["name"]):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command(name="staff", description=s_help["staff_help"])
    # async def help_staff(self, ctx):
    #     await ctx.send(get_msg(self.bot, True))

    @commands.command(name="help", description="Prints help msg")
    @custom_check()
    async def help_user(self, ctx, *args):
        await ctx.send(get_msg(self.bot))


def setup(bot):
    bot.add_cog(Help(bot))
