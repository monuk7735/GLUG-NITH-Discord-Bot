import time

import discord
from discord.ext import commands

import libs.config as config

# async def save_roles():


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Welcome messages for new users
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        dm_channel = await member.create_dm()
        await dm_channel.send(f"Hi {member.mention}!\n\nWelcome to {member.guild.name}!")
        # await dm_channel.send(f"```command prefix is nith\nreply with 'nith help' to know more ```")


def setup(bot):
    bot.add_cog(Welcome(bot))
