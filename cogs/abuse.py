import discord, base64, discum
from discord.ext import commands
from main import prefix, embedColor, accountToken
from utils import *

class Abuse(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='halftoken', description='Get half of a users token.', aliases=['token', 'getusertoken'], usage='')
    async def halftoken(self, ctx, user: discord.User):
        embed = discord.Embed(
            title='Token Finder',
            description=base64.b64encode(str(user.id).encode()).decode(),
            color=embedColor
        )
        await ctx.message.edit(content='', embed=embed)

    @commands.command(name='massmention', description='Ghost mention every user in the channel.', usage='', aliases=['WhatTimeIsIt', 'amogus'])
    @commands.guild_only()
    async def massmention(self, ctx, amount: int = 1):
        try:
            await ctx.message.delete()
        except:
            pass
        print(f'\n{Fore.LIGHTBLUE_EX}[Indigo] {Fore.RESET}Starting to Scrape members')
        # Yes i know this is a bad way to use discord-scum but idc
        DiscumClient = discum.Client(
            token=accountToken, 
            log=True
        )
        message = ''
        DiscumClient.gateway.fetchMembers(str(ctx.guild.id), str(ctx.channel.id))
        @DiscumClient.gateway.command
        def massmention(resp):
            if DiscumClient.gateway.finishedMemberFetching(str(ctx.guild.id)):
                DiscumClient.gateway.removeCommand(massmention)
                DiscumClient.gateway.close()
        DiscumClient.gateway.run()
        # Create a list so that you send the messages faster and ping the most people
        toSend = []
        for memberID in DiscumClient.gateway.session.guild(str(ctx.guild.id)).members:
            print(f'{Fore.LIGHTBLUE_EX}[Indigo] {Fore.RESET}Fetched user {Fore.LIGHTBLUE_EX}{memberID}')
            if len(message) < 1950:
                message += f'<@!{str(memberID)}>ඞ'
            else:
                toSend.append(message)
                message = ''
        toSend.append(message)
        # Send all the messages and instantly delete them
        for i in range(amount):
            for item in toSend:
                logging.print('Sending new message with more pings')
                m = await ctx.send(item)
                logging.print('Sent new message with more pings')
                try:
                    logging.print('Deleting message')
                    # Would use delete_after but this looks better
                    await m.delete()
                    logging.print('Deleted message')
                except:
                    logging.print(f'Failed to delete message')
        # Ask who pinged you and delete the message instantly to look like you're innocent and make it unsnipable
        await ctx.send("who pinged me", delete_after=0)
def setup(client):
    client.add_cog(Abuse(client))
