import requests
import json
import urllib.parse
import os

from bs4 import BeautifulSoup
import discord
from discord.ext import commands

import libs.config as config
from libs.models import Student, Result, Faculty
from libs.command_manager import custom_check, contribute
from libs.embed import officialEmbed
from cogs.help import extract_commands

institute_config = config.get_string("commands")["institute"]

api_key = os.getenv("API_KEY")
api_url = os.getenv("API_URL")
nith_url = "https://nith.ac.in/"

student_by_name = "student_name_search"
faculty_by_name = "faculty_name_search"
student_by_roll = "student_info"
result_using_roll = "result/"


"""
Requests api for data using name and beautifies text using ``` ``` blocks

Also if result is longer tha 2000 characters (Discord Single Msg Limit), It Splits msg into parts providing part number at bottom

Args:
    name: name to search for (Can be Multiple names separated by spaces)

Returns: 
    List of ``` ``` blocks

"""


def search_students_by_name(name):
    data = {
        "query": name,
        "api_key": api_key
    }
    msg = ["```"]
    response = requests.post(api_url + student_by_name, data=data)
    response_json = json.loads(response.text)

    count = 1

    if len(response_json) == 0:
        msg[count-1] += "\nNo Results Found\n"
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
    name: name to search for (Can be Multiple names separated by spaces)

Returns: 
    List of ``` ``` blocks

"""


def search_faculty_by_name(name):
    data = {
        "query": name,
        "api_key": api_key
    }
    msg = ["```"]
    response = requests.post(api_url + faculty_by_name, data=data)
    response_json = json.loads(response.text)

    count = 1

    if len(response_json) == 0:
        msg[count-1] += "\nNo Results Found\n"
        msg[count-1] += "```"
        return msg

    for d in response_json:
        if not "phone" in d:
            continue
        faculty = Faculty(d)
        if len(msg[count-1]) + len(str(faculty)) > 1975:
            count += 1
            msg.append("```")
        msg[count-1] += "\n"+str(faculty)

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
    *   : Sem number

Returns: 
    result_list: If found then list contains student information and result, else an error msg. In either case, needs to be sent to the user.

"""


def result_by_roll(roll, sem):
    try:
        sem = int(sem)
    except ValueError:
        return["```\nInvalid Sem\n```"]

    data = {
        "api_key": api_key
    }

    response = requests.get(
        f"{api_url}{result_using_roll}{roll.lower()}", data=data)

    if response.status_code not in [200, 404]:
        print(response)
        return ["```\nSomething went wrong\n```"]

    try:
        response_json = json.loads(response.text)
    except:
        print(response.text)
        return ["```\nUnknown error occured\n```"]

    if len(response_json) == 0:
        return ["```\nNot Found\n```"]

    result = Result(response_json)

    result_list = result.parse()

    if sem == -1:
        return [result_list[0]+result_list[-1]]

    if sem < 0 or sem > len(result_list[1:]):
        return["```\nInvalid Sem\n```"]

    if sem == 0:
        return ["**Hey there, CoderMan!**",result_list[0] + result_list[1]]
        # return result_list

    return [result_list[0] + result_list[sem]]


"""
Scrapes Official NITH Website to get announcements

Args:
    count: Number of announcements to get

Returns:
    msg: An Embed with all links to announcements
"""


def get_announcements(count):
    response = requests.get(nith_url)

    soup = BeautifulSoup(response.text, 'html.parser')
    embed = officialEmbed("NITH", f"Last {count} announcements")
    embed.set_thumbnail(url=config.get_config("info")["logo"])

    for i, a in enumerate(soup.find('ul', {"class": "allnithlinks"}).findAll('a', {"class": "notranslate"})):
        if i == count:
            break
        link = a.get('href')
        if link.startswith('/'):
            link = nith_url[:-1] + urllib.parse.quote(link)
        link = link.replace(" ", "%20")
        text = a.get_text().strip()
        embed.add_field(name=f"{text}", value=f"[Link]({link})", inline=False)

    return embed


class Institute(commands.Cog, name=institute_config["name"]):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="search", description=institute_config["search"]["description"])
    @custom_check()
    async def search(self, ctx):
        if ctx.invoked_subcommand:
            return
        msg = "```\n"
        msg += "search\n"
        msg += extract_commands(self.search.commands, margin=" ")[1][:-2]
        msg += "```"
        await ctx.channel.send(msg)
        # async with ctx.channel.typing():
        #     messages = await search_by_name(" ".join(args))
        #     for msg in messages:
        #         await ctx.channel.send(msg)

    @search.command(name="student", description=institute_config["search"]["student"]["description"], usage=institute_config["search"]["student"]["usage"])
    async def student_search(self, ctx, *args):
        async with ctx.channel.typing():
            messages = search_students_by_name(" ".join(args))
            for msg in messages:
                await ctx.channel.send(msg)

    @search.command(name="faculty", description=institute_config["search"]["faculty"]["description"], usage=institute_config["search"]["faculty"]["usage"])
    async def faculty_search(self, ctx, *args):
        async with ctx.channel.typing():
            messages = search_faculty_by_name(" ".join(args))
            for msg in messages:
                await ctx.channel.send(msg)

    @commands.command(name="result", description=institute_config["result"]["description"], usage=institute_config["result"]["usage"])
    @custom_check()
    async def result(self, ctx, roll, sem="-1"):
        async with ctx.channel.typing():
            results = result_by_roll(roll, sem)
            for msg in results:
                await ctx.channel.send(msg)

    @commands.command(name="announcements", description=institute_config["announcements"]["description"], usage=institute_config["announcements"]["usage"])
    @custom_check()
    async def announcements(self, ctx, count: int = 5):
        async with ctx.channel.typing():
            msg = get_announcements(count)
            await ctx.channel.send(embed=msg)


def setup(bot):
    bot.add_cog(Institute(bot))
