import json
import random
import os

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingRequiredArgument

import libs.config as config

command_prefixes = config.get_config("prefix")

c_extensions = config.get_config("cogs")
# c_disabled_extensions = config.get_config("disabled_cogs")

# String variables

# Loads the bot's activity status
s_status = config.get_string("status")

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix=command_prefixes, intents=intents, case_insensitive=True)

# Loading the cogs.
if __name__ == "__main__":

    # Remove default help command
    bot.remove_command("help")

    # Logging the loaded cogs.
    if len(c_extensions) != 0:
        print("\nLoading the COGS:")
        for extension in c_extensions:
            try:
                bot.load_extension(extension)
                print(f"[Success]\t{extension} loaded successfully.")
            except Exception as e:
                print(
                    f"[ERROR]\tAn error occurred while loading {extension}\n" + str(e) + "\n")


# Logging the starting of the bot into the console.
@bot.event
async def on_ready():

    # Sets activity message.
    if s_status != "":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=s_status))

    print(f"\n# Logged in as {bot.user}", end="\n\n")

# Removes the "command not found" error from the console.
@bot.event
async def on_command_error(ctx, error):
    error_to_skip = [CommandNotFound, MissingRequiredArgument]

    for error_type in error_to_skip:
        if isinstance(error, error_type):
            return

    raise error

# Starting the bot.
bot.run(os.getenv("TOKEN"))