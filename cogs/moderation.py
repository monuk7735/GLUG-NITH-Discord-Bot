import json
from urllib.parse import uses_fragment

import discord
from discord.ext import commands
from discord.ext.commands import Context

import libs.config as config
from libs.command_manager import custom_check, db_client, extract_member_id, extarct_role_id
from cogs.help import extract_commands

mod_roles = config.get_config("roles")["mod"]
moderation_config = config.get_string("commands")["moderation"]
optional_roles = config.get_config("roles")["optional"]

react_roles_collection = db_client.database.react_roles

"""
Args:
    ctx: Context object

Returns:
    msg: String with member count
"""


async def get_count(ctx):
    msg = "```\n"
    bot_count = 0
    human_count = 0
    for member in ctx.author.guild.members:
        if member.bot:
            bot_count += 1
        else:
            human_count += 1
    msg += f"{'Total Members':20s}: {ctx.author.guild.member_count}\n\n"

    msg += f"{'Humans':20s}: {ctx.author.guild.member_count-bot_count}\n"
    msg += f"{'Bots':20s}: {bot_count}\n\n"

    for role_id in optional_roles:
        role = ctx.guild.get_role(role_id)
        if role:
            msg += f"{role.name:20s}: {len(role.members)}\n"

    msg += "\n```"
    return msg


class Moderation(commands.Cog, name=moderation_config["name"]):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="onCall", description=moderation_config["onCall"]["description"], hidden=True)
    @custom_check(allowed_in_dm=False, req_roles=mod_roles)
    async def change_on_call(self, ctx:Context):
        return

    @change_on_call.command(name="list", description=moderation_config["onCall"]["list"]["description"])
    @custom_check(allowed_in_dm=False, req_roles=mod_roles)
    async def list_on_call(self, ctx:Context):
        all_users = [i for i in db_client.database.on_call.find()]

        on_call_role = ctx.guild.get_role(
            config.get_config("roles")["all"]["on_call"])

        on_call_users = [user.id for user in on_call_role.members]

        msg = "```\n"
        for user in all_users:
            msg += user["name"]
            if user['_id'] in on_call_users:
                msg += " (Current)"
            msg += "\n"
        msg += "```"
        await ctx.send(msg)

    @change_on_call.command(name="add", description=moderation_config["onCall"]["add"]["description"], usage=moderation_config["onCall"]["add"]["usage"])
    @custom_check(allowed_in_dm=False, req_roles=mod_roles)
    async def add_on_call(self, ctx:Context, user_id):
        user = ctx.guild.get_member(extract_member_id(user_id))

        if db_client.database.on_call.find_one({"_id": user.id}):
            await ctx.send("Already added")
            return

        db_client.database.on_call.insert_one({
            "_id": user.id,
            "name": user.name
        })

        await self.list_on_call(ctx)

    @change_on_call.command(name="remove", description=moderation_config["onCall"]["remove"]["description"], usage=moderation_config["onCall"]["remove"]["usage"])
    @custom_check(allowed_in_dm=False, req_roles=mod_roles)
    async def remove_on_call(self, ctx:Context, user_id):
        user = ctx.guild.get_member(extract_member_id(user_id))

        if not db_client.database.on_call.find_one({"_id": user.id}):
            await ctx.send("Not found")
            return

        on_call_role = ctx.guild.get_role(
            config.get_config("roles")["all"]["on_call"])

        db_client.database.on_call.delete_one({"_id": user.id})
        user.remove_roles(on_call_role)

        await self.list_on_call(ctx)

    @change_on_call.command(name="next", description=moderation_config["onCall"]["next"]["description"])
    @custom_check(allowed_in_dm=False, req_roles=mod_roles)
    async def next_on_call(self, ctx:Context):
        all_users = [i for i in db_client.database.on_call.find()]

        on_call_role = ctx.guild.get_role.get_role(
            config.get_config("roles")["all"]["on_call"])

        on_call_users = [user.id for user in on_call_role.members]

        if len(all_users) < 2*len(on_call_users):
            await ctx.channel.send("Need more users")
            return

        next_on_call_users:list = []

        for on_call_user in on_call_users:
            index = 0

            for i, user in enumerate(all_users):
                if user['_id'] == on_call_user:
                    index = i + 1
                    if i == len(all_users) - 1:
                        index = 0
                    while all_users[index]["_id"] in on_call_users + next_on_call_users:
                        index += 1
                        if index >= len(all_users):
                            index = 0
                    break

            next_on_call_users.append(all_users[index]["_id"])

        for user_id in on_call_users:
            member = ctx.guild.get_member(extract_member_id(user_id))
            await member.remove_roles(on_call_role)

        for user_id in next_on_call_users:
            member = ctx.guild.get_member(extract_member_id(user_id))
            await member.add_roles(on_call_role)

        await self.list_on_call(ctx)

    @commands.command(name="stats", description=moderation_config["stats"]["description"], hidden=True)
    @custom_check(allowed_in_dm=False)
    async def stats(self, ctx:Context):
        msg = await get_count(ctx)
        await ctx.channel.send(msg)

    @commands.group(name="reactrole", hidden=True)
    @custom_check(allowed_in_dm=False, req_roles=mod_roles)
    async def react_role(self, ctx:Context):
        if ctx.invoked_subcommand:
            return
        msg = "```\n"
        msg += "reactrole\n"
        msg += extract_commands(self.react_role.commands, margin=" ")[1][:-2]
        msg += "```"

        await ctx.channel.send(msg)

    @react_role.command(name="list", description=moderation_config["reactrole"]["list"]["description"])
    @custom_check(allowed_in_dm=False, req_roles=mod_roles)
    async def list_react_role(self, ctx:Context):
        msg = "```\n"
        msg += f"{'UID':10s}: Title\n"
        for react_role in react_roles_collection.find():
            msg += f"{react_role['uid']:{10}s}: {react_role['title']}\n"
        msg += "```"

        await ctx.send(msg)

    @react_role.command(name="create", description=moderation_config["reactrole"]["create"]["description"], usage=moderation_config["reactrole"]["create"]["usage"])
    @custom_check(allowed_in_dm=False, req_roles=mod_roles)
    async def create_react_role(self, ctx:Context, uid, title):

        # Check if already exists
        if react_roles_collection.find_one({"uid": uid}):
            await ctx.send("Already exists, Use update command")
            return

        react_roles_collection.insert_one({
            "uid": uid,
            "title": title
        })

        await ctx.send(f"Created reactrole category with id:**{uid}** and title:**{title}**")

    @react_role.command(name="delete", description=moderation_config["reactrole"]["delete"]["description"], usage=moderation_config["reactrole"]["delete"]["usage"])
    @custom_check(allowed_in_dm=False, req_roles=mod_roles)
    async def delete_react_role(self, ctx:Context, uid):

        # Check if exists or not
        if not react_roles_collection.find_one({"uid": uid}):
            await ctx.send(f"**{uid}** Not found")
            return

        react_roles_collection.delete_one({"uid": uid})

        await ctx.send(f"Reactrole category with id:**{uid}** deleted")

    @react_role.command(name="genmsg", description=moderation_config["reactrole"]["genmsg"]["description"], usage=moderation_config["reactrole"]["genmsg"]["usage"])
    @custom_check(allowed_in_dm=False, req_roles=mod_roles)
    async def gen_react_role_msg(self, ctx:Context, uid):

        data = react_roles_collection.find_one({"uid": uid})

        data.pop("_id")
        data.pop("uid")
        if "message" in data:
            message_id = data.pop("message")

        # Check if exists or not
        if not data:
            await ctx.send(f"**{uid}** Not found")
            return

        ctx.typing()
        embed = discord.Embed(title=data.pop("title"))
        emojis_to_react = []

        for emoji in data:
            role_id = int(data[emoji].split("\n")[0])
            role_info = "\n".join(data[emoji].split("\n")[1:])
            role = ctx.guild.get_role(role_id)

            embed.add_field(name=f"{emoji}: {role.name}", value=f"{role_info}", inline=False)
            emojis_to_react.append(emoji)

        embed.set_footer(text="React to get role(s)")
        msg = await ctx.send(embed=embed)

        react_roles_collection.update_one(
            {"uid": uid}, {'$set': {"message": msg.id}})

        for emoji in emojis_to_react:
            await msg.add_reaction(emoji)

    @react_role.group(name="update")
    @custom_check(allowed_in_dm=False, req_roles=mod_roles)
    async def update_react_role(self, ctx:Context):
        if ctx.invoked_subcommand:
            return
        msg = "```\n"
        msg += "update\n"
        msg += extract_commands(self.update_react_role.commands,
                                margin=" ")[1][:-2]
        msg += "```"

        await ctx.send(msg)

    @update_react_role.command(name="title", description=moderation_config["reactrole"]["update"]["title"]["description"], usage=moderation_config["reactrole"]["update"]["title"]["usage"])
    @custom_check(allowed_in_dm=False, req_roles=mod_roles)
    async def update_react_role_title(self, ctx:Context, uid, new_title):

        # Check if exists or not
        if not react_roles_collection.find_one({"uid": uid}):
            await ctx.send(f"**{uid}** Not found")
            return

        react_roles_collection.update_one(
            {"uid": uid}, {'$set': {'title': new_title}})

        await ctx.send(f"**{uid}** updatedl: New title **{new_title}**")

    @update_react_role.command(name="set", description=moderation_config["reactrole"]["update"]["set"]["description"], usage=moderation_config["reactrole"]["update"]["set"]["usage"])
    @custom_check(allowed_in_dm=False, req_roles=mod_roles)
    async def update_react_role_add(self, ctx:Context, uid, emoji, role, info):

        # Check if exists or not
        if not react_roles_collection.find_one({"uid": uid}):
            await ctx.send(f"**{uid}** Not found")
            return

        role = ctx.guild.get_role(extarct_role_id(role))
        if not role:
            await ctx.send("Invalid Role")
            return

        react_roles_collection.update_one(
            {"uid": uid}, {'$set': {emoji: f"{role.id}\n{info}"}})

        await ctx.send(f"**{uid}** updated")

    @update_react_role.command(name="remove", description=moderation_config["reactrole"]["update"]["remove"]["description"], usage=moderation_config["reactrole"]["update"]["remove"]["usage"])
    @custom_check(allowed_in_dm=False, req_roles=mod_roles)
    async def update_react_role_remove(self, ctx:Context, uid, emoji):
        # Check if exists or not
        if not react_roles_collection.find_one({"uid": uid}):
            await ctx.send(f"**{uid}** Not found")
            return

        react_roles_collection.update_one(
            {"uid": uid}, {'$unset': {emoji: ""}})

        await ctx.send(f"**{uid}** updated")


def setup(bot):
    bot.add_cog(Moderation(bot))
