import discord
from discord.ext import commands

import libs.config as config
from libs.command_manager import custom_check, get_role


class Stats(commands.Cog, name=stats_config["name"]):
    def __init__(self, bot):
        self.bot = bot

    


def setup(bot):
    bot.add_cog(Stats(bot))
