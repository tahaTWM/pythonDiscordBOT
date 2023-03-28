import datetime
import string
import random

import discord
from discord.ext import commands
import json

intents = discord.Intents.default()
intents.message_content = True


def get_pre(client, message):
    with open('pre.json', 'r') as f:
        pref = json.load(f)

    return pref[str(message.guild.id)]


client = commands.Bot(command_prefix=get_pre, intents=intents)


@client.event
async def on_ready():
    print("Bot is ready")


@client.event
async def on_guild_join(guild):
    with open('pre.json', 'r') as f:
        pref = json.load(f)

    pref[str(guild.id)] = '.'

    with open('pre.json', 'w') as f:
        json.dump(pref, f, indent=4)


@client.command()
async def change_pref(ctx, prefix):
    with open('pre.json', 'r') as f:
        pref = json.load(f)

    pref[str(ctx.guild.id)] = prefix

    with open('pre.json', 'w') as f:
        json.dump(pref, f, indent=4)

    await ctx.send(f'prefix is change to {prefix}')


@client.command()
async def gPassword(ctx, length):
    leng = int(length)
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(leng))

    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    with open('passwords.json', 'w') as f:
        json.dump(f"{current_time} : {password}", f, indent=4)

    return await ctx.send(f'your password is: {password}')


@client.command()
async def time(ctx):
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return await ctx.send(f'your password is: {current_time}')


# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
client.run("MTA4ODQwMzc0Mzg5ODM1MzcwNQ.G4AUkr.T3suZPgafynXtxI0bnqQerwsf-0xBaBoFtLC_0")
