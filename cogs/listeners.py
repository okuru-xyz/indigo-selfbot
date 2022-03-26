import discord, base64, discum, httpx, datetime, re, threading, logging
from discord.ext import commands
from main import accountToken, nitroSniper
from utils import *

class Listeners(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.checkedCodes = []

    def snipeNitro(self, content: str):
        if('discord.gift/' in content and nitroSniper):
            startTime = datetime.datetime.now()
            code = re.search(
                pattern='discord.gift/(.*)',
                string=content
            ).group(1)
            
            if(code in self.checkedCodes):
                return(logging.printError(f'Code {code} was already sent.'))

            if len(code) in [16, 24]:
                headers = {
                    'user-agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FSL 7.0.5.01003)',
                    'authorization': accountToken
                }

                request = httpx.post(
                    f'https://discordapp.com/api/v9/entitlements/gift-codes/{code}/redeem', 
                    headers=headers,
                ).text

                elapsedTime = datetime.datetime.now() - startTime
                elapsedTime = f'{elapsedTime.seconds}.{elapsedTime.microseconds}'

                if 'subscription_plan' in request:
                    logging.print(f'| NITRO | Redeemed code {code}')

                elif 'This gift has been redeemed already.' in request:
                    logging.printError(f'| NITRO | Code {code} already redeemed.')

                elif 'Unknown Gift Code' in request:
                    logging.printError(f'| NITRO | {code} is Invalid!')
                
                print(f'{Fore.RESET}> {Fore.LIGHTCYAN_EX}Elapsed: {elapsedTime}')
                return(self.checkedCodes.append(code))
            
    @commands.command(name='togglesniper', description='Toggle one of the snipers.', usage='')
    async def togglesniper(self, ctx, sniper: str = 'nitro'):
        return await ctx.message.edit(content='> Coming soon.')
        # Code below is test
        sniper = sniper.lower()
        if sniper == 'nitro':
            global nitroSniper
            nitroSniper = False
            print('Disabled Nitro Sniper.')
        elif sniper == 'spam':
            print('Disabled Spam Sniper.')
    
    @commands.Cog.listener()
    async def on_message(self, message):
        threading.Thread(target=self.snipeNitro, args=(message.content,)).start()

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
