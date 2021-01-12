import libs.config as config
import discord

configAuthor = config.get_config("info")["name"]
configAuthor_img = config.get_config("info")["logo"]
configFooter = config.get_config("info")["footer"]
configColor = config.get_config("colors")["embed"]


def officialEmbed(title, desc, color=configColor, author=configAuthor, author_img=configAuthor_img, footer=configFooter, url=""):
    embed = discord.Embed(
        title=title,
        description=desc,
        color=color, url=url)
    embed.set_author(name=author, icon_url=author_img)
    embed.set_footer(text=footer)

    return embed
