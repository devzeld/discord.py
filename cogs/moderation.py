import discord
from discord.ext import commands
import os
import json

if os.path.exists(os.getcwd() + "/config.json"):
    
    with open("./config.json") as f:
        configData = json.load(f)

else:
    configTemplate = {"Token": "", "bannedWords": []}

    with open("./config.json", "w+") as f:
        json.dump(configTemplate, f)


token = configData["Token"]
bannedWords = configData["bannedWords"]


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation is on")

    @commands.command()
    @commands.has_permissions(administrator= True)
    async def add_ban_word(self, ctx, word):
        if word.lower() in bannedWords:
            await ctx.send("Already banned")
        else:
            bannedWords.append(word.lower())
            
            with open("./config.json", "r+") as f:
                data = json.load(f)
                data["bannedWords"] = bannedWords
                f.seek(0)
                f.write(json.dumps(data))
                f.truncate()
            
            await ctx.message.delete()
            await ctx.send("word added to banned words.")

    @commands.command()
    @commands.has_permissions(administrator= True)
    async def remove_ban_word(self, ctx, word):
        if word.lower() in bannedWords:
            bannedWords.remove(word.lower())
            
            with open("./config.json", "r+") as f:
                data = json.load(f)
                data["bannedWords"] = bannedWords
                f.seek(0)
                f.write(json.dumps(data))
                f.truncate()
            
            await ctx.message.delete()
            await ctx.send("word added to banned words.")
        else:
            await ctx.send("word isn't banned.")    

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def add_text_channel(self, ctx, name):
        await ctx.guild.create_text_channel(name)
        await ctx.send(f"{name} created")


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def delete_channel(self, ctx, channel: discord.TextChannel):
        await channel.delete()
        await ctx.send(f"{channel.name} deleted")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, user: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await user.add_roles(role)
        await ctx.send(f"{str(user).split('#')[0]} muted")

    @commands.command()
    @commands.has_permissions(ban_members=True, kick_members=True)
    async def unmute(self, ctx, user: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await user.remove_roles(role)
        await ctx.send(f"{str(user).split('#')[0]} unmuted")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def create_role(self, ctx, name):
        guild = ctx.guild
        await guild.create_role(name=name)
        await ctx.send(f'Role `{name}` has been created')


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def giverole(self, ctx, user: discord.Member, role: discord.Role):
        if role in user.roles:
            await ctx.send(f"The user '{user}' already has the role '{role.name}'")
        else:
            await user.add_roles(role)
            await ctx.send(f"The role '{role.name}' has been added to {str(user).split('#')[0]}")

    @commands.command()
    @commands.has_permissions(manage_roles= True)
    async def removerole(self, ctx, user: discord.Member, role: discord.Role):
        if role in user.roles:
            await ctx.send(f"The role '{role.name}' has been removed from '{user}'")
            await user.remove_roles(role)


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason= None): 
        guild = ctx.guild
        await member.kick(reason=reason)
        await member.send(f'{member.mention}, You have been kicked from {guild}, because: {reason}')
        await ctx.send(f"{member.mention} banned for {reason}, by {ctx.author}")


    @commands.command()
    @commands.has_permissions(ban_members= True)
    async def ban(self, ctx, member: discord.Member, reason = None):
        guild = ctx.guild
        await member.ban(reason= reason)
        await member.send(f'{member.mention}, You have been banned from {guild}, because: {reason}.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.User):
        guild = ctx.guild
        await guild.unban(member)
        await member.send(f'Bravo, {member.mention}, se stato sbannato')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def banned_users_list(self, ctx):
        user = ctx.author
        guild_bans = await ctx.guild.bans()
        guild_banned_users = []
        
        for x in guild_bans:
            guild_banned_users.append(f"User: {x.user.name.split('#')[0]}, id: {x.user.id}")
        
        embed= discord.Embed(title= "Banned User List", colour= discord.Colour.blurple())
        embed.add_field(name= "Total Members:",value= f"{len(guild_bans)}")
        embed.add_field(name= "Members:", Value= f"{guild_banned_users}", inline= False) 
        
        await user.send(content= None, embed= embed)
    
    @commands.command()
    @commands.has_permissions(administrator= True)
    async def change_user_name(self, ctx, user: discord.Member, name):
        await ctx.send(f"{user.name} changed to {name}")
        await user.edit(nick=name)
        


def setup(bot):
    bot.add_cog(Moderation(bot))
