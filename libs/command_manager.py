import functools

# import libs.config as config
from libs.embed  import officialEmbed

"""
Any and all checks common to more than one command should be performed here
"""

def custom_check():

    """Decorator for any checks.

    Wrap around a bot command to check appropriate permission and channel context of the executed command from
    the Context object provided by the bot's event listener method, and errors out if checks do not pass.

    Example Usage:
        @commands.command...
        @custom_check()
        def echo...

    Args:
        None yet

    Returns:
        Original method call that the method wraps around, and continues executing the command/method.
        If any checks fail, then will stop execution of the method and returns False after raising an exception.
    """

    def guild_check(cmd):

        @functools.wraps(cmd)
        async def wrapper(*args, **kwargs):
            ctx = args[1]
            # if type(ctx) is not commands.Context:
            #     print("ERROR: Missing ctx variable in @check() call in", cmd.__name__, " command!")
            #     raise commands.MissingRequiredArgument(ctx)
            # if ctx.author.guild.id not in config.get_config("authorised_servers"):
            #     await ctx.channel.send(config.get_string("error")["server_not_authorised"])
            #     return False

            if ctx.author.name != "monuk7735":
                return False


            return await cmd(*args, **kwargs)

        return wrapper

    return guild_check

"""
Function to send contribution embed as reply

Args:
    ctx: context variable which is passed to a command function

Returns:
    None
"""

async def contribute(ctx):
    embed = officialEmbed("Contribute", "Contribute to this project, help create more cool features", url=config.get_config("info")["url"])
    embed.set_thumbnail(url=config.get_string("logos")["github"])
    await ctx.send(embed=embed)
