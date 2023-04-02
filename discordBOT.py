import asyncio

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
async def start_chat(message):
    user = message.author
    channel = await user.create_dm()  # create a direct message channel with the user
    await channel.send('Hello, this is your bot speaking!\n'
                       'I can do all those this things\n'
                       'change prefix -> change_pref\n'
                       'create Stron Password -> pword\n'
                       'send the created password to your Email -> save_password')  # send a message to the user


client.run("MTA4ODQwMzc0Mzg5ODM1MzcwNQ.Gt3gem.1bhngsjv-WH_qdv0kPf0eA5VrbUbhlba5g2X5Q")
