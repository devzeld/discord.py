import discord
from discord.ext import commands

class Vocal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Vocal is on")
        
    @commands.command()
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send("You are not connected to a voice channel!")
            return
        else:
            channel = ctx.message.author.voice.channel
            user = ctx.message.author.mention
            await ctx.send(f"{user}, Now I am connected to {channel}")
            await ctx.message.add_reaction('✅')
        await channel.connect()


    @commands.command()
    async def leave(self, ctx):
        voice_client = ctx.message.guild.voice_client
        user = ctx.message.author.mention
        channel = ctx.author.voice.channel
        if not voice_client:
            await ctx.send(f"{user}, I am not connected to a voice cahnnel!")
        else:
            await voice_client.disconnect()
            await ctx.send(f"{user}, Disconnected to {channel}")
            await ctx.message.add_reaction('✅')    
        


def setup(bot):
    bot.add_cog(Vocal(bot))