import discord
from discord.ext import commands
from main import prefix, embedColor

class Text(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name='purgehack', description='Clear a chat without permission.', usage='')
    async def purgehack(self, ctx):
        await ctx.message.edit(content='ﾠﾠ\n'* 400 + 'ﾠﾠ')

def setup(client):
    client.add_cog(Text(client))
