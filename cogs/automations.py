import time
import random

import discord
from discord.ext import commands, tasks

import libs.config as config
from libs.command_manager import db_client

welcome_channel_id = config.get_config("channels")["hello-world"]
welcome_quotes = config.get_string("welcome")
rules_array = config.get_string("rules")


class Automate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.change_on_call.start()

    # Welcome messages for new users
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(welcome_channel_id)
        # msg = random.choice(welcome_quotes).format(member.mention)
        # await channel.send(msg)

        dm_channel = await member.create_dm()
        # await dm_channel.send(f"Hi {member.mention}!\n\nWelcome to {member.guild.name}!")
        # await dm_channel.send(f"```command prefix is nith\nreply with 'nith help' to know more ```")

    # Called When a Message is Pinned
    @commands.Cog.listener()
    async def on_guild_channel_pins_update(self, channel, last_pin_time):
        bot_test = self.bot.get_channel(config.get_config("channels")["glug-bot-test"])
        last_pin = await channel.pins()

        if last_pin_time:
            await bot_test.send(f"New Message pinned in {channel.name}")
        else:
            await bot_test.send(f"Message unpinned in {channel.name}")

        if last_pin_time:
            last_pin = last_pin[-1]
            db_client.database.pinned_messages.insert_one({
                "_id":last_pin.id,
                "author": last_pin.author.name,
                "author_id": last_pin.author.id,
                "created_at": str(last_pin.created_at),
                "jump_url": str(last_pin.jump_url)
            })

        # TODO Make a PR on CSEC Github Repo with new Pinned Message

    # @tasks.loop(seconds=7)
    # async def change_on_call(self):
    #     print("Loop")


def setup(bot):
    bot.add_cog(Automate(bot))
