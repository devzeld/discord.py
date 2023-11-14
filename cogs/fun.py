import random
import discord
from discord.ext import commands
from variabili import kick_giff, kick_name, punch_giff, punch_name
import aiohttp
import qrcode as qr
import os
import mimetypes

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun is on")
    
    @commands.command()
    async def hi(self, ctx):
        await ctx.send(f'Hi, {ctx.author.mention}')

    @commands.command()
    async def hi_to(self, ctx, member: discord.Member):
        await ctx.send(f'Hi, {member.mention}')

    @commands.command()
    async def random_num(self, ctx, min, max):
        rn = random.randrange(int(min), int(max))
        await ctx.send(f"||{str(rn)}||")

    @commands.command()
    async def choose(self, ctx, arg1, arg2):
        choice = random.choice([arg1, arg2])
        await ctx.send(f"||{choice}||")
        
    @commands.command()
    async def say(self, ctx, arg):
        await ctx.send(arg)

    @commands.command()
    async def coinflip(self, ctx):
        choice = ['Testa', 'Croce']
        randomcoin = random.choice(choice)
        await ctx.send(randomcoin)
        
    @commands.command()
    async def rock_paper_scissors(self, ctx, your_choice):
        possible_choices = ["rock", "paper", "scissors"]
        client_choice = random.choice(possible_choices)

        async def you_win():
            await ctx.send(f"you {your_choice}, client {client_choice}. you win, Yey")

        async def client_wins():
            await ctx.send(f"you {your_choice}, client {client_choice}. the client wins, oh no")

        if your_choice in possible_choices:
            if your_choice != client_choice:
                if "rock" in your_choice and "paper" in client_choice:
                    await client_wins()
                elif "scissors" in your_choice and "paper" in client_choice:
                    await you_win()
                elif "scissors" in your_choice and "rock" in client_choice:
                    await client_wins()
                elif "rock" in your_choice and "scissors" in client_choice:
                    await you_win()
                elif "paper" in your_choice and "rock" in client_choice:
                    await you_win()
                elif "paper" in your_choice and "scissors" in client_choice:
                    await client_wins()
            else:
                await ctx.send(f"{your_choice}, {client_choice} tie")
        else:
            await ctx.send(f"{your_choice} is not in possible_choices")


    @commands.command()
    async def kicks(self, ctx):
        kick_gif = discord.Embed(
            colour=(discord.Colour.gold()),
            description=f'{ctx.author.mention} {(random.choice(kick_name))}'
        )
        kick_gif.set_image(url=(random.choice(kick_giff)))

        await ctx.send(embed=kick_gif)


    @commands.command()
    async def punch(self, ctx):
        punch_gif = discord.Embed(
            colour=(discord.Colour.gold()),
            description=f'{ctx.author.mention} {(random.choice(punch_name))}'
        )
        punch_gif.set_image(url=(random.choice(punch_giff)))

        await ctx.send(embed=punch_gif)
    
    @commands.command()
    async def r(self,ctx, name):
        async with aiohttp.ClientSession() as cs:
            try:
                async with cs.get(f'https://www.reddit.com/r/{name}.json') as r:
                    memesjson = await r.json()
                    memeembed = discord.Embed(color= discord.Color.orange())
                    memes = memesjson["data"]["children"][random.randint(0, 25)]["data"]["url"]
                    filetype = mimetypes.MimeTypes().guess_type(memes)[0]
                    while filetype == None:
                        memes = memesjson["data"]["children"][random.randint(0, 25)]["data"]["url"]
                        filetype = mimetypes.MimeTypes().guess_type(memes)[0]
                        
                    memeembed.set_image(url= memes)
                    memeembed.set_footer(text= f'Powered by r/{name} | Post requested by {ctx.author}')
                    await ctx.send(embed=memeembed)
                
            except:
                    embed = discord.Embed(title= "Sorry there's nothing here", description= f"We couldn't find nothing in r/{name}. \n Or the subreddit that you write don't exist.", color= discord.Color.dark_red())
                    await ctx.send(embed= embed)
                
    @commands.command()
    async def qrcode(self, ctx):
        content = ctx.message.content.split("!qrcode ")[1]
        code = qr.make(content)
        filename = f"{str(ctx.author._user.id)}qrcode.png"
        a = code.save(filename)
        
        await ctx.send(file= discord.File(filename))
        os.remove(filename)


def setup(bot):
    bot.add_cog(Fun(bot))