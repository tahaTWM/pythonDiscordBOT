import asyncio
import datetime
import smtplib
import string
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import discord
from discord.ext import commands
import json

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='', intents=intents)


@client.event
async def on_ready():
    print("Bot is ready")


@client.command()
async def great(ctx):
    """Sends a greeting message in a direct message."""
    await ctx.author.send(f'Hello, {ctx.author.name}!')


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
async def save_password(ctx, email):
    send_email(email)
    return await ctx.send("check your Email with subject 'Discord Bot Password'")


@client.command()
async def delete_dm(ctx):
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


def send_email(email):
    # Set up the email sender and receiver addresses
    sender = "cs.17.037@student.uotechnology.edu.iq"
    receiver = email

    # Create the message object
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = "Discord Bot Password"

    # fetch data from json file
    with open("passwords.json", 'r') as f:
        PandH = json.load(f)

    last_item_key = list(PandH.keys())[-1]
    last_item_value = list(PandH.values())[-1]

    # Add the message body
    body = f"your Password '{last_item_value}' just create for '{last_item_key}'"
    message.attach(MIMEText(body, 'plain'))

    # Log in to your email account
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, "0135555331")

    # Send the email
    text = message.as_string()
    server.sendmail(sender, receiver, text)

    # Log out of your email account
    server.quit()


client.run("")
