import re
import time
from datetime import datetime
import random
import json
import os

import discord
from discord_slash import SlashCommand
from discord.ext import commands, tasks

import aiohttp

if os.path.exists(os.getcwd() + "/config.json"):

    with open("./config.json") as f:
        configData = json.load(f)

else:
    configTemplate = {"Token": "", "bannedWords": [], "noPing": []}

    with open("./config.json", "w+") as f:
        json.dump(configTemplate, f)

token = configData["Token"]
bannedWords = configData["bannedWords"]
noPing = configData["noPing"]


def msg_contains_word(msg, word):
    return re.search(fr'\b({word})\b', msg) is not None


def get_prefix(bot, message):
    prefixes = ['!!', 'lol', '!']

    if not message.guild:
        return '?'

    return commands.when_mentioned_or(*prefixes)(bot, message)


allintents = discord.Intents.all()
intents = discord.Intents.default()
intents.members = True

# bot = discord.Client(intents=discord.Intents.all())
bot = commands.Bot(command_prefix=get_prefix, intents=allintents, help_command=None)


@bot.event
async def on_ready():
    # When the bot is online he change he's status and he's activity
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing, name='prefix(>!)'),
        status=discord.Status.idle)

    # He print in the console the on_ready function
    print('Connected to bot: {}'.format(bot.user.name))
    print('He says "Botto is on"')
    print('Bot ID: {}'.format(bot.user.id))


@bot.event
async def on_message(message):
    user = message.author
    zeld = await bot.fetch_user(697510535935033406)

    if message.guild != None:
        username = str(message.author).split("#")[0].lower()
        msg = message.content
        channel = str(message.channel.name)
        server = str(message.guild.name)
        try:
            print(
                f"user: {username}, msg: {msg}, channel: {channel}, server: {server},")
        except:
            print("usrnf")

    elif message.author != bot.user:

        print(f"dm: '{message.content}' by: {message.author}")
        embed = discord.Embed(
            title=f"Direct Message from {message.author}", description=f"content: {message.content}.", color=user.color)
        embed.set_thumbnail(url=message.author.avatar_url)
        embed.timestamp = datetime.utcnow()
        await zeld.send(embed=embed)

    if any(word in message.content for word in noPing):
        await message.delete()
        await message.author.send("You cannot tag that user.")

    messageAuthor = message.author
    if bannedWords != None and (isinstance(message.channel, discord.channel.DMChannel) == False):
        for BannedWord in bannedWords:
            if msg_contains_word(message.content.lower(), BannedWord):
                await message.delete()
                await messageAuthor.send(
                    f"{messageAuthor.mention} your massage was removed as it contained a banned word.")

    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.author.send('Invalid command used!')
    if isinstance(error, commands.MissingPermissions):
        await ctx.author.send("You don't have the permissions!")
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.author.send("The client don't have the permissions for this command!")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.author.send('The command that you use is not complete, try use the argument that you need.')
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.author.send('Wait some time before use another command!')


#   else:
#        await ctx.author.send('There is an error.')

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')


@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(token)
