import random
import discord
from discord.ext import commands
from main import bot
import json

with open ("./config.json") as f:
    configData = json.load(f)
    
noPing= configData["noPing"]


class Utility(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Utility is on")
    
    @commands.command()
    async def noping(self, ctx, member: discord.Member):
        noPing.append(member.mention)
        
        with open("./config.json", "r+") as f:
            data = json.load(f)
            data["noPing"] = noPing
            f.seek(0)
            f.write(json.dumps(data))
            f.truncate()
        
        await ctx.send(f"{member.name} was added to the noPing list.")
    
    
    @commands.command()
    async def serverinfo(self, ctx):
        guild = ctx.guild
        roles: list[discord.Role] = guild.roles
        channels = guild.channels
        user = ctx.author

        infoembed = discord.Embed(title=f"Server Info:", color=user.color)

        infoembed.add_field(name='Server Name:',
                            value=f'{guild.name}', inline=False)
        infoembed.add_field(name='Server Tot. Members:',
                            value=f'{len(guild.members)}', inline=False)
        infoembed.add_field(name='Server Owner Name:',
                            value=f'{guild.owner.display_name}', inline=False)
        infoembed.add_field(name='Server Tot. Roles:',
                            value=f'{len(roles)}', inline=False)
        infoembed.add_field(name='Server Tot. Channels:',
                            value=f'{len(channels)}', inline=False)

        infoembed.set_footer(text=f'Requested by - {ctx.author}',
                            icon_url=ctx.author.avatar_url)

        await user.send(embed=infoembed)
        
    @commands.command()
    async def members(self, ctx):
        users = ctx.guild.members
        users_name = []
        for x in users:
            users_name.append(x.name)

        await ctx.send(f"there are {ctx.guild.member_count} members, {users_name}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)
        await ctx.author.send(f'Done. Deleted {amount} messages')
    
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def spam_in(self, ctx, spam_message, times, channel: discord.TextChannel):
        i = 0
        times = int(times)
        await ctx.send(f"spamming '{spam_message}' in {channel.mention} for {times} times")
        while i < int(times):
            await channel.send(spam_message)
            i += 1


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def spam_in_dm(self, ctx, user: discord.Member, content: discord.Message, number_of_messages: int):
        i = 0
        await ctx.send(f"spamming {str(user.name).split('#')[0]} with {content} for {number_of_messages} times")
        while i < number_of_messages:
            await user.send(content)
            i += 1
    
    @commands.command()
    async def get_user_Id(self, ctx, user: discord.Member):
        id = user.mention.split("@")[1].split(">")[0]
        await ctx.send(f"{str(user).split('#')[0]}'s id: {id}")
        
    @commands.command()
    async def ranmember(self, ctx):
        members = ctx.guild.members
        membersA = []
        for x in members:
            membersA.append(x.mention)
        await ctx.send(f"||{random.choice(membersA)}||")


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def all_members_by_role(self, ctx, role: discord.Role):
        all_members = ctx.guild.members
        role_members = []
        for x in all_members:
            if role in x.roles:
                role_members.append(x.name)
        await ctx.send(f"{role.mention}'s users {role_members}")
    
    @commands.command()
    async def see_avatar(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author

            for x in roles:
                print(x.name)

            embed = discord.Embed(
                title=f"Avatar of {member.mention}", color=role._colour)
            embed.set_image(url=avatar)

            await ctx.send(embed=embed)
        else:
            avatar = member._user.avatar_url
            roles: list[discord.Role] = member.roles
            role: discord.Role = roles[len(
                roles) - 1] if roles != None else print("none")
            embed = discord.Embed(
                title="Avatar", description=f"{member.mention} avatar", color=role._colour)
            embed.set_image(url=avatar)

            await ctx.send(content= None, embed=embed)


    @commands.command()
    async def info_of(self, ctx, user: discord.Member= None):

        if user == None:
            user = ctx.author

        rlist = []
        for role in user.roles:
            if role.name != '@everyone':
                rlist.append(role.mention)

        b = ','.join(rlist)

        embed = discord.Embed(color=user.color)

        embed.set_author(name=f'User info - {user}'),
        embed.set_thumbnail(url=user.avatar_url),
        embed.set_footer(text=f'Requested by - {ctx.author}',
                        icon_url=ctx.author.avatar_url)

        embed.add_field(name='ID: ', value=user.id, inline=False)
        embed.add_field(name='Name: ', value=user.display_name, inline=False)
        embed.add_field(name='Ping: ', value=user.mention, inline=False)

        embed.add_field(name='Joined at: ', value=user.joined_at.strftime(
        '%b %d, %Y, %T'), inline=False)

        embed.add_field(name=f'Roles:({len(rlist)})',
                            value=''.join([b]), inline=False)

        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def change_channel_position(self, ctx, channel: discord.TextChannel, position: discord.CategoryChannel):
        await channel.edit(category=position)
        await ctx.send(f"{channel.mention} moved to position {position}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dm_all(self, ctx, role: discord.Role, content):
        guild: discord.Guild = ctx.guild
        members: list[discord.Member] = guild.members
        membersRole = []
        await ctx.send(f"dming all {role.mention} with {content}")
        for x in members:
            if role in x.roles:
                membersRole.append(x)
        for x in membersRole:
            await x.send(content)
    
    @commands.command()
    async def an(self, ctx, bot):
        #!-an <id del canale> [title(jsahdj) content(hjsdfjk) color(dark_red)]
        if ctx.guild == None:
            channel: discord.TextChannel = await bot.fetch_channel(int(ctx.message.content.split("<")[1].split(">")[0]))
            content = ctx.message.content.split("[")[1].split("]")[0]
            title = content.split("title(")[1].split(")")[0]
            colorname = content.split("color(")[1].split(")")[0]
            content = content.split("content(")[1].split(")")[0]

            try:
                color = getattr(discord.Color, colorname)
            except:
                color = None
            embed = discord.Embed(title=title, description=content,
                                color=discord.Color.dark_purple() if color == None else color())
            await channel.send(content=None, embed=embed)


    @commands.command()
    async def suggest(self, ctx):
        suggestion = ctx.message.content.split("!-suggest")[1]
        suggestionChannel = await bot.fetch_channel(973266934185472030)
        embed = discord.Embed(title= f"Suggerimento Inviato", description= f"**{ctx.author.mention} il tuo suggerimento e' stato inviato in {suggestionChannel.mention}**", color= discord.Color.gold())
        embed.set_thumbnail(url= ctx.author._user.avatar_url)
        await ctx.send(embed= embed)
        embed = discord.Embed(title= f"Suggerimento di {str(ctx.author._user.name).split('#')[0]}", description= f"**{ctx.author.mention} ha suggerito**\n{suggestion}", color= discord.Color.gold())
        embed.set_thumbnail(url= ctx.author._user.avatar_url)
        embed.set_footer(text= f"{str(ctx.author._user.name).split('#')[0]} ID is {ctx.author._user.id}", icon_url= ctx.author._user.avatar_url)
        suggestionmessage = await suggestionChannel.send(content= None, embed= embed)
        await suggestionmessage.add_reaction("👍")
        await suggestionmessage.add_reaction("👎") 
    
    @commands.command()
    async def showguilds(self, ctx):
        user = ctx.author
        message = ""
        for guild in bot.guilds:
            message += f"{guild.name}\n"
        guildembed = discord.Embed(title='Show Guilds', color=user.color)
        guildembed.add_field(name="Number of server's:",
                            value=f'{len(bot.guilds)}', inline=False)
        guildembed.add_field(name="Server's:", value=f'{message}', inline=False)
        await user.send(content= None, embed=guildembed)
        await ctx.send('Sending the showguilds infos in private.')
    
    @commands.command()
    @commands.is_owner()
    async def create_role_atPosition(self, ctx, name, position=None):
        guild: discord.Guild = ctx.guild
        roles = await guild.fetch_roles()
        lenRoles = len(roles)
        role = await guild.create_role(name=name)
        await role.edit(position= lenRoles - 1)
        await ctx.send(f"created {name}")


def setup(bot):
    bot.add_cog(Utility(bot))