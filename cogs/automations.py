import time
import random
from pprint import pprint

import discord
from discord.ext import commands, tasks
from discord.raw_models import RawReactionActionEvent

import libs.config as config
from libs.command_manager import db_client

welcome_channel_id = config.get_config("channels")["hello-world"]
welcome_quotes = config.get_string("welcome")
rules_array = config.get_string("rules")

react_roles_collection = db_client.database.react_roles


class Automate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.messages = {}
        self.messages_counter = {}
        # self.change_on_call.start()
    
    @tasks.loop(seconds=5)
    async def reset_counter(self):
        self.messages = {}
        self.messages_counter = {}

    # Welcome messages for new users
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(welcome_channel_id)
        # msg = random.choice(welcome_quotes).format(member.mention)
        # await channel.send(msg)

        dm_channel = await member.create_dm()
        # await dm_channel.send(f"Hi {member.mention}!\n\nWelcome to {member.guild.name}!")
        # await dm_channel.send(f"```command prefix is glug\nreply with 'glug help' to know more ```")

    # Called When a Message is Pinned
    @commands.Cog.listener()
    async def on_guild_channel_pins_update(self, channel, last_pin_time):
        bot_test = self.bot.get_channel(
            config.get_config("channels")["glug-bot-test"])
        last_pin = await channel.pins()

        if last_pin_time:
            await bot_test.send(f"New Message pinned in {channel.name}")
        else:
            await bot_test.send(f"Message unpinned in {channel.name}")

        if last_pin_time:
            last_pin = last_pin[-1]
            db_client.database.pinned_messages.insert_one({
                "_id": last_pin.id,
                "author": last_pin.author.name,
                "author_id": last_pin.author.id,
                "created_at": str(last_pin.created_at),
                "jump_url": str(last_pin.jump_url)
            })

        # TODO Make a PR on CSEC Github Repo with new Pinned Message

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, raw_reaction: RawReactionActionEvent):
        guild = self.bot.get_guild(raw_reaction.guild_id)
        emoji = str(raw_reaction.emoji)

        member = guild.get_member(raw_reaction.user_id)

        if member.bot:
            return

        data = react_roles_collection.find_one(
            {"message": raw_reaction.message_id})

        if not data:
            return

        if not emoji in data:
            return

        role_id = int(data[emoji].split("\n")[0])
        role = guild.get_role(role_id)

        print(f"Adding {role.name} to {member.name}")
        await member.add_roles(role, reason=f"they reacted with {raw_reaction.emoji.name} to {data['uid']}")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, raw_reaction: RawReactionActionEvent):
        guild = self.bot.get_guild(raw_reaction.guild_id)
        emoji = str(raw_reaction.emoji)

        member = guild.get_member(raw_reaction.user_id)

        if member.bot:
            return

        data = react_roles_collection.find_one(
            {"message": raw_reaction.message_id})

        if not data:
            return

        if not emoji in data:
            return

        role_id = int(data[emoji].split("\n")[0])
        role = guild.get_role(role_id)

        print(f"Removing {role.name} from {member.name}")
        await member.remove_roles(role, reason=f"they removed {raw_reaction.emoji.name} reaction from {data['uid']}")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if message.author.bot:
            return

        count = len(message.content)

        if str(message.author.id) not in self.messages:
            self.messages[str(message.author.id)] = message.content
            return

        if self.messages[str(message.author.id)] == message.content:
            await message.channel.send("Spam Detected")
        else:
            self.messages[str(message.author.id)] = message.content


def setup(bot):
    bot.add_cog(Automate(bot))
