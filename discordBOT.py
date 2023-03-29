import asyncio
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


@client.event
async def on_member_join(member):
    await member.send(
        'Hi! Welcome to our server, in 30 seconds you will get "Verified" '
        'role, please read rules in that time.')
    await asyncio.sleep(30)
    verifiedRole = discord.utils.get(member.guild.roles, id="1090756064674336928")
    await member.add_roles(verifiedRole)


@client.command()
async def pword(ctx, length, hint):
    leng = int(length)
    characters = string.ascii_letters + string.digits + "!#$%&()*+-.:;<=>?@[]^_`{|}"
    password = ''.join(random.choice(characters) for i in range(leng))

    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    # read the password file
    with open('passwords.json', 'r') as f:
        pword = json.load(f)

    pword[str(hint)] = "".join(password)

    # write on password file
    with open('passwords.json', 'w') as f:
        json.dump(pword, f, indent=4)

    return await ctx.send(f"{hint} = {password} \nif you want to save password in"
                          "type -save_password + your email")

    # return await ctx.send(f"{hint} = {password}")


@client.command()
async def time(ctx):
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return await ctx.send(f'{current_time}')


# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
client.run("")
