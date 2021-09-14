import discord, base64, discum
from discord.ext import commands
from main import prefix, embedColor, accountToken
from utils import *

class Listeners(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name='togglesniper', description='Toggle one of the snipers.', usage='')
    async def togglesniper(self, ctx, sniper: str = 'nitro'):
        return await ctx.message.edit(content='> Coming soon.')
        # Code below is test
        sniper = sniper.lower()
        if sniper == 'nitro':
            print('Disabled Nitro Sniper.')
        elif sniper == 'spam':
            print('Disabled Spam Sniper.')
        
    @commands.Cog.listener()
    async def on_command(self, ctx):
        print(f'{Fore.LIGHTBLUE_EX}[Indigo] {Fore.RESET}Used command: {ctx.message.clean_content}')
    
    @commands.Cog.listener()
    async def on_connect(self):
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
    {Fore.LIGHTBLUE_EX}Account: {Fore.RESET}{self.client.user}
    {Fore.LIGHTBLUE_EX}Status: {Fore.LIGHTGREEN_EX}Connected
    {Fore.BLUE}{'_' * 100}
        ''')


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send(f'> **Error**: {error}')
        
def setup(client):
    client.add_cog(Listeners(client))
