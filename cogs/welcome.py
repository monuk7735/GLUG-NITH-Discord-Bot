import time
import random

import discord
from discord.ext import commands

import libs.config as config

welcome_channel_id = config.get_config("channels")["hello-world"]
welcome_quotes = config.get_string("welcome")
rules_array = config.get_string("rules")

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Welcome messages for new users
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(welcome_channel_id)
        msg = random.choice(welcome_quotes).format(member.mention)
        await channel.send(msg)

        # dm_channel = await member.create_dm()
        # await dm_channel.send(f"Hi {member.mention}!\n\nWelcome to {member.guild.name}!")
        # await dm_channel.send(f"```command prefix is nith\nreply with 'nith help' to know more ```")


def setup(bot):
    bot.add_cog(Welcome(bot))
