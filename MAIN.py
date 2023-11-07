import discord
from discord.ext import commands
import youtube_dl

from random import choice


intents = discord.Intents.default()
intents.members = True

bot= commands.Bot(command_prefix="%", intents=intents, help_command=None)



@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(
        type=discord.ActivityType.listening, name="%help | .gg/sinners"
    ))
    print("Hello, Your bot is ready to use")


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"User {member} has been kicked.")

@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member : discord.Member, *, reason=None, arg=None):
    if arg == None: ("Please specify a user you would like to ban")
    await member.ban(reason=reason)
    await ctx.send(f"User {member} has been banned.")

@bot.command()
@commands.has_permissions(administrator=True)
async def unban(ctx,*,member):
    banned_users = await ctx.guild.bans()
    member_name, member_disc = member.split('#')

    for banned_entry in banned_users:
        user = banned_entry.user

        if(user.name, user.discriminator)==(member_name,member_disc):
            await ctx.guild.unban(user)
        await ctx.send(member_name +" has been unbanned!")
        return

    await ctx.send(member+" was not found")


@bot.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, reason: str = None):
        muted = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(muted)
        await ctx.send(f"{member} has been muted")


@bot.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member, reason: str = None):
        muted = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(muted)
        await ctx.send(f"{member} has been unmuted")


@bot.command()
async def credits(ctx):
    await ctx.send("Made by 3lines")
    await ctx.send("Join my server discord.gg/sinners")
    
    







class BotData:
    def __init__(self):
        self.welcome_channel = None

botdata = BotData()


@bot.command()
async def hey(ctx):
    channel = ctx.channel
    await channel.send("hey lol " + str(ctx.author.mention))

@bot.command()
async def ping(ctx, arg=None):
    if arg == " @ ":
        await ctx.channel.send("You did it wrong.")

    else:
        await ctx.channel.send(str(ctx.author.mention)  +  "  Hey, hows your day going ")

@bot.command()
async def repeat (ctx,  *, arg=None):
    if arg == None:
        await ctx.channel.send ("You forgot to say what you wanted me to repeat.")
    else:
        await ctx.channel.send( " " + str(arg))

@bot.event 
async def on_member_join(member):
    if botdata.welcome_channel != None:
        await botdata.welcome_channel.send(f"Welcome, make sure to invite your friends and boost us! {member.mention}")

    else:
        print("Welcome channel was not set.")

@bot.command()
async def set_welcome_channel(ctx, channel_name=None):
    if channel_name != None:
        for channel in ctx.guild.channels:
            if channel.name == channel_name:
                botdata.welcome_channel = channel
                await ctx.channel.send(f"welcome channel has been set to: {channel.name}")
                await channel.send ("This is now the welcome channel!")

async def get_help_embed():
    em = discord.Embed(title="Help!" , description="", color=15790320)
    em.description += f"**{bot.command_prefix}** **kick **─** kicks the member you mention **\n"
    em.description += f"**{bot.command_prefix}** **ban **─** bans the member you mention**\n"
    em.description += f"**{bot.command_prefix}** **mute **─** mutes the member you mention **\n"
    em.description += f"**{bot.command_prefix}** **dm **─** dms a specific user 'dm userid message' **\n"
    em.description += f"**{bot.command_prefix}** **dma **─** dms a message to all the users in the server**\n" 
    em.description += f"**{bot.command_prefix}** **hey **─** replies to you with hey lol**\n" 
    em.description += f"**{bot.command_prefix}** **ping **─** find out :) **\n"
    em.description += f"**{bot.command_prefix}** **repeat **─** repeats your message**\n"
    em.description += f"**{bot.command_prefix}** **snipe **─** logs the last deleted message**\n"
    em.description += f"**{bot.command_prefix}** **userinfo **─** Gives the date they joined discord, the server and their highest role**\n"
  
    em.set_image(url="https://i.pinimg.com/originals/7e/54/80/7e5480fb12d7b827a76e83ebce347bd5.gif")
    em.set_footer(text="Thanks for using ex, dm 3lines with any questions" ,icon_url=bot.user.avatar_url)
    return em




@bot.command()
async def help(ctx):
    em = discord.Embed(title="Help!" , description="", color=15790320)
    em.description += f"**{bot.command_prefix}** **kick **─** kicks the member you mention **\n"
    em.description += f"**{bot.command_prefix}** **ban **─** bans the member you mention**\n"
    em.description += f"**{bot.command_prefix}** **mute **─** mutes the member you mention **\n"
    em.description += f"**{bot.command_prefix}** **dm **─** dms a specific user 'dm userid message' **\n"
    em.description += f"**{bot.command_prefix}** **dma **─** dms a message to all the users in the server**\n" 
    em.description += f"**{bot.command_prefix}** **hey **─** replies to you with hey lol**\n" 
    em.description += f"**{bot.command_prefix}** **ping **─** find out :) **\n"
    em.description += f"**{bot.command_prefix}** **repeat **─** repeats your message**\n"
    em.description += f"**{bot.command_prefix}** **snipe **─** logs the last deleted message**\n"
    em.description += f"**{bot.command_prefix}** **userinfo **─** Gives the date they joined discord, the server and their highest role**\n"
    
    em.set_image(url="https://i.pinimg.com/originals/7e/54/80/7e5480fb12d7b827a76e83ebce347bd5.gif")
    em.set_footer(text="Thanks for using ex, dm 3lines#6666 with any questions" ,icon_url=bot.user.avatar_url) 


    await ctx.send(embed=em)

bot.sniped_messages = {}

@bot.event
async def on_message_delete(message):
    bot.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)

@bot.command()
async def snipe(ctx):
    contents, author, channel_name, time = bot.sniped_messages[ctx.guild.id]

    embed = discord.Embed(description=contents, color=discord.Color.random(), timestamp=time)
    embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
    embed.set_footer(text=f"Deleted in : #{channel_name}")

    await ctx.channel.send(embed=embed)
    

@bot.command()
async def userinfo(ctx, member: discord.Member):
    roles = [role for role in member.roles]


    embed = discord.Embed(color=discord.Color.random(), timestamp=ctx.message.created_at)

    embed.set_author(name=f"User Info = {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
   
    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Guild name:", value=member.display_name)

    embed.add_field(name="Created at:" , value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
    embed.add_field(name="Top role:", value=member.top_role.mention)
    
    embed.add_field(name="Bot?", value=member.bot)

    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def dm(ctx, user_id=None, *, args=None):
    if user_id != None and args != None:
        try:
            target = await bot.fetch_user(user_id)
            await target.send(args)

            await ctx.channel.send("'" + args + " Has been sent to: " + target.name)

        except:
            await ctx.channel.send ("Couldn't dm the given user.")

    else:
        await ctx.channel.send("A user_id and/or arguments were not included.")

@bot.command()
@commands.has_permissions(administrator=True)
async def dma(ctx, *, args=None):
    if args != None:
        members = ctx.guild.members
        for member in members:
            try:
                await member.send(args)
                print("'" + args + " Sent to: " + member.name)

            except:
                print ("Couldn't send '" + args + "' to " + member.name)

        else:
            await ctx.channel.send("You didn't provide arguments.")




bot.run("INSERT TOKEN HERE")
