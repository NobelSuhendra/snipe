import discord
import os
from discord.ext import commands
import json
from datetime import datetime

intents = discord.Intents(messages=True, guilds=True, members=True)

prefixs = '?'
bot = commands.Bot(command_prefix=prefixs, intents=intents)
delmsg = {}


@bot.event
async def on_ready():
    global delmsg
    print(f"Successfully logged in as {bot.user}!")
    with open("store.json", "r") as read_file:
        data = json.load(read_file)
        delmsg = json.loads(data)
    print(delmsg)
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name="for deleted messages"))


@bot.event
async def on_message_delete(ctx):
    if not ctx.author.bot:
        global delmsg
        print(ctx.id)
        delmsg[str(
            ctx.id)] = [ctx.content,
                        str(ctx.author),
                        str(datetime.now())]
        os.remove("store.json")
        open("store.json", 'w').close()
        newdat = json.dumps(delmsg)
        with open("store.json", "w") as write_file:
            json.dump(newdat, write_file)
        embed = discord.Embed(
            title=f'**{ctx.author}** deleted:\n "{ctx.content}"')
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)


@bot.command()
async def snipe(ctx):
    global delmsg
    embed = discord.Embed(title=f"**SNIPED!**\n\n─────────────")
    for messages in reversed(list(delmsg.keys())):
        embed.add_field(
            name=
            f"\n**{delmsg[messages][1]}** deleted ({delmsg[messages][2]}):",
            value=f'"{delmsg[messages][0]}"\n ───────────────',
            inline=False)
    embed.set_author(name=f"Requested by {ctx.author}",
                     icon_url=ctx.author.avatar_url)
    await ctx.channel.send(embed=embed)


bot.run(os.getenv('token'))
