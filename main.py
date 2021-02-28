import asyncio
from os import getenv
import datetime as dt
from sys import prefix
import os
import youtube_dl

import discord
from discord.ext import commands
from discord import guild, client, message
from discord.ext import commands, tasks

# Start of the bot
from py import path

intents = discord.Intents().default()
intents.members = True
BOT_TOKEN = getenv("BOT_TOKEN", None)
bot = commands.Bot(command_prefix='.', intents=intents)


# This is so the bot is ready to do stuff
@bot.event
async def on_ready():
    print('ready')
    when_it_day.start()
    when_it_day2.start()


# posts a picture of a troll face !trolled
@bot.command(name='trolled')
async def trolled(ctx):
    await ctx.send(file=discord.File(rf'./pictures/trollface.png'))


# plays a sound when someone plays the command !music
@bot.command(name='music')
async def game_music(ctx):
    channel = await ctx.message.author.voice.channel.connect()
    channel.play(discord.FFmpegPCMAudio(rf'./audio/gamemusic.mp3'))


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


# Grabs the day and uploads the file corresponding
@tasks.loop(hours=24)
async def when_it_day2():
    day = dt.date.today().strftime("%A").lower()
    print(day)
    message_channel = bot.get_channel(705124613599920199)
    await message_channel.send(file=discord.File(rf'./videos/{day}.mp4'))


# What time of the day it is
@when_it_day2.before_loop
async def before_when_it_day2():
    for _ in range(60 * 60 * 24):  # loop the whole day
        # print(dt.datetime.now().hour)
        if dt.datetime.now().hour == 12:  # 24 hour format
            print('It is time')
            return
        await asyncio.sleep(1)  # wait a second before looping again. You can make it more


@bot.event
async def on_member_join(member):
    if member.dm_channel is None:
        await member.create_dm()
    await member.send('''Why did you join this server. Oh well too late now.''')


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


def endSong(path):
    os.remove(path)


@bot.command(pass_context=True)
async def play(ctx, url, vc=None):
    if not ctx.message.author.voice:
        await ctx.send(
            'You are not connected to a voice channel')  # message when you are not connected to any voice channel
        return

    else:
        channel = ctx.message.author.voice.channel

        voice_client = await channel.connect()
    path = ''

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            file = ydl.extract_info(url, download=True)
            path = './' + str(file['title']) + "-" + str(file['id'] + ".mp3")

        voice_client.play(discord.FFmpegPCMAudio(path), after=lambda x: endSong(path))
        voice_client.source = discord.PCMVolumeTransformer(voice_client.source, 1)
    except:
        await ctx.send('No fool')
        vc = ctx.message.guild.voice_client
        await vc.disconnect()
        return
    voice_client = await channel.connect()
    await ctx.send(f'**Music: **{url}')  # sends info about song playing right now


qcount = 0


@bot.command()
async def queue(ctx):
    global qcount
    if qcount <= 6:
        qcount += 1
        await ctx.send('Added to the queue!' f'{ctx.author.mention}')
    else:
        await ctx.send('Queue full')


@bot.command()
async def stop(ctx):
    await ctx.message.delete()
    vc = ctx.message.guild.voice_client
    if vc is None:
        await ctx.send("You silly, I'm not in any VCs right now.")
    else:
        await vc.disconnect()


# runs the bot
bot.run(BOT_TOKEN, bot=True, reconnect=True)
