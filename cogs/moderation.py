import discord
from discord.ext import commands

import libs.config as config
from libs.command_manager import custom_check, get_role, db_client, get_member

mod_roles = config.get_config("roles")["mod"]
moderation_config = config.get_string("commands")["moderation"]

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
        role = get_role(ctx, role_id)
        if role:
            msg += f"{role.name:20s}: {len(role.members)}\n"

    msg += "\n```"
    return msg


class Moderation(commands.Cog, name=moderation_config["name"]):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="onCall",description=moderation_config["onCall"]["description"], hidden=True)
    @custom_check(allowed_in_dm=False, req_roles=mod_roles)
    async def change_on_call(self, ctx):
        return

    @change_on_call.command(name="list", description=moderation_config["onCall"]["list"]["description"])
    @custom_check(allowed_in_dm=False, req_roles=mod_roles)
    async def list_on_call(self, ctx):
        all_users = [i for i in db_client.database.on_call.find()]

        on_call_role = get_role(
            ctx, config.get_config("roles")["all"]["on_call"])

        on_call_users = [user.id for user in on_call_role.members]

        msg = "```\n"
        for user in all_users:
            msg += user["name"]
            if user['_id'] in on_call_users:
                msg += " (Current)"
            msg += "\n"
        msg += "```"
        await ctx.channel.send(msg)

    @change_on_call.command(name="add",description=moderation_config["onCall"]["add"]["description"], usage=moderation_config["onCall"]["add"]["usage"])
    @custom_check(allowed_in_dm=False, req_roles=mod_roles)
    async def add_on_call(self, ctx, user_id):
        user = get_member(ctx, user_id)

        if db_client.database.on_call.find_one({"_id": user.id}):
            await ctx.channel.send("Already added")
            return

        db_client.database.on_call.insert_one({
            "_id": user.id,
            "name": user.name
        })

        await self.list_on_call(ctx)

    @change_on_call.command(name="remove",description=moderation_config["onCall"]["remove"]["description"], usage=moderation_config["onCall"]["remove"]["usage"])
    @custom_check(allowed_in_dm=False, req_roles=mod_roles)
    async def remove_on_call(self, ctx, user_id):
        user = get_member(ctx, user_id)

        if not db_client.database.on_call.find_one({"_id": user.id}):
            await ctx.channel.send("Not found")
            return

        on_call_role = get_role(
            ctx, config.get_config("roles")["all"]["on_call"])

        db_client.database.on_call.delete_one({"_id": user.id})
        user.remove_roles(on_call_role)

        await self.list_on_call(ctx)

    @change_on_call.command(name="next", description=moderation_config["onCall"]["next"]["description"])
    @custom_check(allowed_in_dm=False, req_roles=mod_roles)
    async def next_on_call(self, ctx):
        all_users = [i for i in db_client.database.on_call.find()]

        on_call_role = get_role(
            ctx, config.get_config("roles")["all"]["on_call"])

        on_call_users = [user.id for user in on_call_role.members]

        if len(all_users) < 2*len(on_call_users):
            await ctx.channel.send("Need more users")
            return

        next_on_call_users = []

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

        for user in on_call_users:
            member = get_member(ctx, user)
            await member.remove_roles(on_call_role)

        for user in next_on_call_users:
            member = get_member(ctx, user)
            await member.add_roles(on_call_role)

        await self.list_on_call(ctx)

    @commands.command(name="stats", description=moderation_config["stats"]["description"], hidden=True)
    @custom_check(allowed_in_dm=False)
    async def stats(self, ctx):
        msg = await get_count(ctx)
        await ctx.channel.send(msg)


def setup(bot):
    bot.add_cog(Moderation(bot))
