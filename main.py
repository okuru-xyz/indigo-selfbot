import discord, discum, json, os, sys, base64, asyncio, random
from discord.ext import commands
from colorama import Fore, init

sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=37, cols=100))

init()

config = json.load(open('config.json'))
account_token = config.get('Discord Token')
prefix = config.get('Command Prefix')


# Will add customization later list
embed_color = 0x3964c3


client = discord.Client()
client = commands.Bot(
    command_prefix=prefix,
    case_insensitive=True,
    help_command=None,
    auto_reconnect=True,
    self_bot=True
)



'''
Event Handlers
'''
@client.event
async def on_connect():
    os.system('cls; clear')
    logo = f'''{Fore.LIGHTCYAN_EX}
██╗███╗   ██╗██████╗ ██╗ ██████╗  ██████╗ 
██║████╗  ██║██╔══██╗██║██╔════╝ ██╔═══██╗
██║██╔██╗ ██║██║  ██║██║██║  ███╗██║   ██║
██║██║╚██╗██║██║  ██║██║██║   ██║██║   ██║
██║██║ ╚████║██████╔╝██║╚██████╔╝╚██████╔╝
╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝ ╚═════╝  ╚═════╝'''
    for line in logo.split('\n'):
        print(line.center(100))
    print(f'''
{Fore.LIGHTBLUE_EX}Account: {Fore.RESET}{client.user}
{Fore.LIGHTBLUE_EX}Status: {Fore.LIGHTGREEN_EX}Connected
{Fore.BLUE}{'_' * 100}
    ''')
@client.event
async def on_command(ctx):
    print(f'{Fore.LIGHTBLUE_EX}[Indigo] {Fore.RESET}Used command: {ctx.message.clean_content}')

@client.event
async def on_command_error(ctx, error):
    await ctx.send(f'> **Error**: {error}')


'''
Commands
'''
@client.command(name='help', description='Show help menu', usage='')
async def help(ctx):
    embed = discord.Embed(
        title='Help',
        description=f'''
        Arguments in `[]` are required, arguments in `()` are optional.
        
        **`{prefix}`massmention(amount)** » Mention lots of users in a guild
        **`{prefix}`whattimeisit (amount)** » Alias for Mass mention
        **`{prefix}`token [User]** » Get half of a user's token''',
        color=embed_color
    )
    await ctx.message.edit(content='', embed=embed)



@client.command(name="massmention", description="Ghost mention every user in the guild that can see the channel", usage="", aliases=['WhatTimeIsIt'])
@commands.guild_only()
async def massmention(ctx, amount: int = 1):
    try:
        await ctx.message.delete()
    except:
        pass
    print(f'\n{Fore.LIGHTBLUE_EX}[Indigo] {Fore.RESET}Starting to Scrape members')
    DiscumClient = discum.Client(token=account_token, log=True)
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
        print(f'{Fore.LIGHTBLUE_EX}[Indigo] {Fore.RESET}Fetched user {Fore.LIGHTBLUE_EX}{memberID}')
        if len(message) < 1950:
            message += f"<@!{str(memberID)}>ඞ"
        else:
            tosend.append(message)
            message = ""
    tosend.append(message)
    # Send all the messages and instantly delete them
    for i in range(amount):
        for item in tosend:
            print(f'\n{Fore.LIGHTBLUE_EX}[Indigo] {Fore.RESET}Sending new message with more pings')
            m = await ctx.send(item)
            print(f'{Fore.LIGHTBLUE_EX}[Indigo] {Fore.RESET}Sent new message with more pings')
            try:
                print(f'{Fore.LIGHTBLUE_EX}[Indigo] {Fore.RESET}Deleting message')
                # Would use delete_after but this looks better
                await m.delete()
                print(f'{Fore.LIGHTBLUE_EX}[Indigo] {Fore.RESET}Deleted message')
            except:
                print(f'{Fore.LIGHTBLUE_EX}[Indigo] {Fore.RESET}Failed to delete message')
    # Ask who pinged you and delete the message instantly to look like you're innocent and make it unsnipable
    await ctx.send("who pinged me", delete_after=0)


@client.command(name='token', description='Get half of a users token', aliases=['gettoken', 'halftoken', 'getusertoken'], usage='')
async def token(ctx, user: discord.User):
    embed = discord.Embed(
        title='Token Finder',
        description=base64.b64encode(str(user.id).encode()).decode(),
        color=embed_color
    )
    await ctx.message.edit(content='', embed=embed)
    
try:
    client.run(
        account_token#,
        # No longer needed as we're using discord.py-self: bot=False
    )
except Exception as e:
    print(e)
    print('Invalid Token')
