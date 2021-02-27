import asyncio
from os import getenv
import datetime as dt

import discord
from discord.ext import commands, tasks

# Start of the bot
intents = discord.Intents().default()
BOT_TOKEN = getenv("BOT_TOKEN", None)
bot = commands.Bot(command_prefix='lol', intents=intents)


# This is so the bot is ready to do stuff
@bot.event
async def on_ready():
    print('ready')
    when_it_day.start()


@bot.command(name='trolled')
async def trolled(ctx):
    await ctx.send(
        'https://www.google.com/url?sa=i&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FTrollface&psig=AOvVaw1pApt7pamTZaOWj2Ky-b7s&ust=1614541302151000&source=images&cd=vfe&ved=0CA0QjhxqFwoTCLCriJjpiu8CFQAAAAAdAAAAABAD')


# Grabs the day and uploads the file corresponding
@tasks.loop(hours=24)
async def when_it_day():
    day = dt.date.today().strftime("%A").lower()
    print(day)
    message_channel = bot.get_channel(740037079102259221)
    await message_channel.send(file=discord.File(rf'./videos/{day}.mp4'))


# What time of the day it is
@when_it_day.before_loop
async def before_when_it_day():
    for _ in range(60 * 60 * 24):  # loop the whole day
        # print(dt.datetime.now().hour)
        if dt.datetime.now().hour == 12:  # 24 hour format
            print('It is time')
            return
        await asyncio.sleep(1)  # wait a second before looping again. You can make it more


# runs the bot
bot.run(BOT_TOKEN, bot=True, reconnect=True)
