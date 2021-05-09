import time

from discord_slash import SlashCommand, SlashCommandOptionType, SlashContext
from discord import Client

import libs.config as config
import cogs.institute as InstituteCog

guild_id = [643486522003161111]


def start(client: Client):
    slash = SlashCommand(client, sync_commands=True, sync_on_cog_reload=True )

    update_slash_commands(slash)


def update_slash_commands(slash: SlashCommand):

    @slash.slash(name=config.get_slash("result")['name'], description=config.get_slash("result")['description'], guild_ids=guild_id, options=config.get_slash("result")['options'])
    async def result(ctx, roll: int, sem: int = -1):
        await ctx.defer()
        result = InstituteCog.result_by_roll(roll, sem)
        await ctx.send("".join(result))

    @slash.slash(name=config.get_slash("search")['name'], description=config.get_slash("search")['description'], guild_ids=guild_id, options=config.get_slash("search")['options'])
    async def search(ctx, search_for, name: str):
        await ctx.defer()
        if search_for == "0":
            search_result = InstituteCog.search_students_by_name(name)
        else:
            search_result = InstituteCog.search_faculty_by_name(name)

        for message in search_result:
            await ctx.send(message)

    @slash.slash(name=config.get_slash("announcements")['name'], description=config.get_slash("announcements")['description'], guild_ids=guild_id, options=config.get_slash("announcements")['options'])
    async def announcements(ctx: SlashContext, count=5):
        await ctx.defer()
        announcements_embed = InstituteCog.get_announcements(count)
        await ctx.send("", embed=announcements_embed)
