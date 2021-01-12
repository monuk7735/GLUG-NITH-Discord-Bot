import requests
import json

import discord
from discord.ext import commands

import libs.config as config

from libs.models import Student, Result
from libs.command_manager import custom_check, contribute

url = "https://nith-app-greyhats.herokuapp.com/"
student_by_name = "student_name_search"
student_by_roll = "student_info"
result_using_roll = "result"


"""
Requests api for data using name and beautifies text using ``` ``` blocks

Also if result is longer tha 2000 characters (Discord Single Msg Limit), It Splits msg into parts providing part number at bottom

Args:
    name: name to search for (Can be Multiple names separated by spaces)

Returns: 
    List of ``` ``` blocks

"""


async def search_by_name(name):
    data = {
        "query": name
    }
    msg = ["```"]
    response = requests.post(url + student_by_name, data=data)
    response_json = json.loads(response.text)

    count = 1

    if len(response_json) == 0:
        msg[count-1] += "No Results Found"
        msg[count-1] += "```"
        return msg

    for d in response_json:
        student = Student(d)
        if len(msg[count-1]) + len(str(student)) > 1975:
            count += 1
            msg.append("```")
        msg[count-1] += "\n"+str(student)

    if count > 1:
        for i in range(count):
            msg[i] += f"\n{i+1}/{count}```"
    else:
        msg[count-1] += "```"
    return msg

"""
Requests api for data using name and beautifies text using ``` ``` blocks

Also if result is longer tha 2000 characters (Discord Single Msg Limit), It Splits msg into parts providing part number at bottom

Args:
    roll: Roll number to get result for

Returns: 
    String Result in ``` ``` blocks

"""


async def result_by_roll(roll):
    data = {
        "rollno": roll.lower()
    }

    msg = "```"
    response = requests.post(url + result_using_roll, data=data)

    if len(response.text) == 0:
        msg += "No Results Found"
        msg += "```"
        return msg

    response_json = json.loads(response.text)

    result = Result(response_json)
    msg += str(result)

    msg += "```"
    return msg


class Institute(commands.Cog, name=config.get_string("description")["help"]["name"]):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="search", description=config.get_string("description")['institute']['search'], usage="{Name}")
    @custom_check()
    async def search(self, ctx, *args):
        print(args)
        async with ctx.channel.typing():
            messages = await search_by_name(" ".join(args))
            for msg in messages:
                await ctx.channel.send(msg)

    @commands.command(name="result", description=config.get_string("description")['institute']['result'], usage="{Roll}")
    @custom_check()
    async def result(self, ctx, roll):
        # msg = await result_by_roll(roll)
        await ctx.channel.send("```Yet to be implemented.```")
        await contribute(ctx)


def setup(bot):
    bot.add_cog(Institute(bot))
