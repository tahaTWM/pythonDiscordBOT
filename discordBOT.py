import asyncio
import datetime
import string
import random
import mailtrap as mt

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

    return await ctx.send(f"{hint} = {password} \nif you want to save the password in your Email"
                          " type '-save_password + your email' ")

    # return await ctx.send(f"{hint} = {password}")


@client.command()
async def time(ctx):
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    send_email()
    return await ctx.send(f'{current_time}')


def send_email():
    mail = mt.Mail(
        sender=mt.Address(email="cs.17.037@student.uotechnology.edu.iq", name="TWM test"),
        to=[mt.Address(email="taha.twm.1234@gmail.com")],
        subject="You are awesome!",
        text="Congrats for sending test email with Mailtrap!",
    )
    clent = mt.MailtrapClient(token="ac5373bf20d4120313c84a5d42fb63c7")
    clent.send(mail)


client.run("")
