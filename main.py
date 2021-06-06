import discord, discum, json, os
from discord.ext import commands
from colorama import Fore, init

init()

config = json.load(open('config.json'))
token = config.get('Discord Token')
prefix = config.get('Command Prefix')

client = commands.Bot(
    command_prefix=prefix,
    case_insensitive=True,
    help_command=None,
    self_bot=True
)

@client.event
async def on_connect():
    os.system('cls; clear')
    print(f'''{Fore.LIGHTCYAN_EX}
██╗███╗   ██╗██████╗ ██╗ ██████╗  ██████╗ 
██║████╗  ██║██╔══██╗██║██╔════╝ ██╔═══██╗
██║██╔██╗ ██║██║  ██║██║██║  ███╗██║   ██║
██║██║╚██╗██║██║  ██║██║██║   ██║██║   ██║
██║██║ ╚████║██████╔╝██║╚██████╔╝╚██████╔╝
╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝ ╚═════╝  ╚═════╝ 
{Fore.LIGHTBLUE_EX}[Indigo] {Fore.RESET}Logged in as {Fore.LIGHTBLUE_EX}{client.user}''')

@client.event
async def on_command(ctx):
    print(f'{Fore.LIGHTBLUE_EX}[Indigo] {Fore.RESET}Used command: {ctx.message.clean_content}')

@client.event
async def on_command_error(ctx, error):
    await ctx.send(f'> **Error**: {error}')

@client.command()
async def help(ctx):
    embed = discord.Embed(
        title='Help',
        description=f'''
            **`{prefix}`massmention** » Mention lots of users in a guild
            **`{prefix}`whattimeisit** » Alias for Mass mention''',
        color=0x3964c3
    )
    await ctx.message.edit(content='', embed=embed)

@client.command(name="massmention", description="Ghost mention every user in the guild that can see the channel", usage="", aliases=['WhatTimeIsIt'])
@commands.guild_only()
async def massmention(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    DiscumClient = discum.Client(token=token)
    message = ""
    DiscumClient.gateway.fetchMembers(str(ctx.guild.id), str(ctx.channel.id))
    @DiscumClient.gateway.command
    def massmention(resp):
        if DiscumClient.gateway.finishedMemberFetching(str(ctx.guild.id)):
            DiscumClient.gateway.removeCommand(massmention)
            DiscumClient.gateway.close()
    DiscumClient.gateway.run()
    # Create a list so that you send the messages faster and ping the most people
    tosend = []
    for memberID in DiscumClient.gateway.session.guild(str(ctx.guild.id)).members:
        if len(message) < 1950:
            message += f"<@!{str(memberID)}>ඞ"
        else:
            tosend.append(message)
            message = ""
    tosend.append(message)
    # Send all the messages and instantly delete them
    for item in tosend:
        await ctx.send(item, delete_after=0)

    # Ask who pinged you and delete the message instantly to look like you're innocent and make it unsnipable
    await ctx.send("who pinged me", delete_after=0)


try:
    client.run(
        token,
        bot=False
    )
except :
    print('Invalid Token')
