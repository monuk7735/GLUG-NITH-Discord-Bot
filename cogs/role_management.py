import time
import asyncio

import discord
from discord.ext import commands
from discord.ext.commands import Context

import libs.config as config
from libs.command_manager import custom_check, delete_messages
from cogs.help import extract_commands

role_manager_config = config.get_string("commands")["role_manager"]


def extract_roles(ctx, *args):
    valid_roles = []
    invalid_role_ids = []
    for role_id in args:
        if role_id.lower() in config.get_config("roles")["all"]:
            role = ctx.guild.get_role(config.get_config("roles")[
                                      "all"][role_id.lower()])
        else:
            role = None
        if role:
            valid_roles.append(role)
        else:
            invalid_role_ids.append(role_id)
    return (valid_roles, invalid_role_ids)


# async def delete_message(ctx:Context, *messages):
#     await asyncio.sleep(15)
#     await ctx.channel.delete_messages(iter(messages))


class RoleManager(commands.Cog, name=role_manager_config["name"]):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="opt", pass_context=True)
    @custom_check(allowed_channels=['i-can-help-with'], allowed_in_dm=False)
    async def opt(self, ctx:Context):
        if ctx.invoked_subcommand:
            return
        msg = "```\n"
        msg += "opt\n"
        msg += extract_commands(self.opt.commands, margin=" ")[1][:-2]
        msg += "```"

        sent = await ctx.channel.send(msg)
        await delete_messages(ctx, ctx.message, sent)

    @opt.command(name="list", description=role_manager_config["opt"]["list"]["description"])
    @custom_check(allowed_channels=['i-can-help-with'], allowed_in_dm=False)
    async def opt_list(self, ctx:Context):
        msg = "```\n"
        for role in config.get_config("roles")["optional"]:
            role = ctx.guild.get_role(str(role))
            msg += f"{role.name}\n"
        msg += "```"
        sent = await ctx.channel.send(msg)

        await delete_messages(ctx, ctx.message, sent)

    @opt.command(name="out", description=role_manager_config["opt"]["out"]["description"], usage=role_manager_config["opt"]["out"]["usage"])
    @custom_check(allowed_channels=['i-can-help-with'], allowed_in_dm=False)
    async def opt_out(self, ctx:Context, *args):
        if len(args) == 0:
            await ctx.channel.send("Need some roles to opt out of")
            return

        valid_roles, invalid_role_ids = extract_roles(ctx, *args)

        flags = [False] * 3
        assigned = "Unassigned  : "
        not_allowed = "Not Allowed : "
        error = "Not Found   : "

        if len(valid_roles) > 0:
            for role in valid_roles:

                if role.id in config.get_config("roles")["optional"]:
                    await ctx.author.remove_roles(role)
                    assigned += f"{role.name} "
                    flags[0] = True
                else:
                    not_allowed += f"{role.name} "
                    flags[1] = True

        if len(invalid_role_ids) > 0:
            for role in invalid_role_ids:
                error += f"{role} "
                flags[2] = True
        msg = "```\n"
        if flags[0]:
            msg += f"{assigned}\n\n"
        if flags[1]:
            msg += f"{not_allowed}\n\n"
        if flags[2]:
            msg += f"{error}\n\n"
        msg += "```"

        sent = await ctx.channel.send(msg)
        await delete_messages(ctx, ctx.message, sent)

    @opt.command(name="in", description=role_manager_config["opt"]["in"]["description"], usage=role_manager_config["opt"]["in"]["usage"])
    @custom_check(allowed_channels=['i-can-help-with'], allowed_in_dm=False)
    async def opt_in(self, ctx:Context, *args):
        if len(args) == 0:
            await ctx.channel.send("Need some roles to opt into")
            return
        valid_roles, invalid_role_ids = extract_roles(ctx, *args)

        flags = [False] * 3
        assigned = "Assigned   : "
        not_allowed = "Not Allowed: "
        error = "Not Found  : "

        if len(valid_roles) > 0:
            for role in valid_roles:
                if role.id in config.get_config("roles")["optional"]:
                    await ctx.author.add_roles(role)
                    assigned += f"{role.name} "
                    flags[0] = True
                else:
                    not_allowed += f"{role.name} "
                    flags[1] = True

        if len(invalid_role_ids) > 0:
            for role in invalid_role_ids:
                error += f"{role} "
                flags[2] = True
        msg = "```\n"
        if flags[0]:
            msg += f"{assigned}\n\n"
        if flags[1]:
            msg += f"{not_allowed}\n\n"
        if flags[2]:
            msg += f"{error}\n\n"
        msg += "```"

        sent = await ctx.channel.send(msg)
        await delete_messages(ctx, ctx.message, sent)


def setup(bot):
    bot.add_cog(RoleManager(bot))
