import asyncio
import datetime
import ssl
import string
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 2525
    SMTP_USERNAME = 'cs.17.037@student.uotechnology.edu.iq'
    SMTP_PASSWORD = ''

    # Sender and recipient
    FROM_EMAIL = 'cs.17.037@student.uotechnology.edu.iq'
    TO_EMAIL = 'taha.twm.123@gmail.com'

    # Email content
    message = 'Subject: Test email from Mailtrap\n\n'
    message += 'Hello, this is a test email from Mailtrap'

    # Connect to Mailtrap's SMTP server
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(FROM_EMAIL, TO_EMAIL, message)


@client.command()
async def start_chat(message):
    user = message.author
    channel = await user.create_dm()  # create a direct message channel with the user
    await channel.send('Hello, this is your bot speaking!\n'
                       'I can do all those this things\n'
                       'change prefix -> change_pref\n'
                       'create Stron Password -> pword\n'
                       'send the created password to your Email -> save_password')  # send a message to the user


@client.command()
async def delete(ctx):
    dm_channel = await ctx.author.create_dm()
    messages_to_delete = []
    async for message in dm_channel.history(limit=10):
        messages_to_delete.append(message)

    print(len(messages_to_delete))

    deleted_count = 0
    for message in messages_to_delete:
        await message.delete()
        deleted_count += 1
        await asyncio.sleep(0.5)
    await ctx.send(f'{deleted_count} messages deleted.')


client.run("")
