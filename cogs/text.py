from socket import MSG_DONTROUTE
from click import edit
import discord, base64
from discord.ext import commands
from main import prefix, editMSG

class Text(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name='purgehack', description='Clear a chat without permission.', usage='')
    async def purgehack(self, ctx):
        await ctx.message.edit(content='ﾠﾠ\n'* 400 + 'ﾠﾠ')

    @commands.command(name='secretify', description='Add ||this|| to all characters in message.', usage='')
    async def secretify(self, ctx, *, message: str):
        out = ''
        for letter in message:
            out += f'||{letter}||'
        await ctx.message.edit(content=out)

    @commands.command(name='b64encode', description='Encode a base64 message.', usage=' [message]', aliases=['base64encode'])
    async def b64encode(self, ctx, *, message: str):
        try:
            decoded = base64.b64encode(message.encode()).decode()
        except:
            decoded = '**Error**: Failed to encode.'
        embed = discord.Embed(
            title='Base64 Encode',
            description=decoded
        )
        await editMSG(ctx, embed)

    @commands.command(name='b64decode', description='Decode a base64 message.', usage=' [message]', aliases=['base64decode'])
    async def b64decode(self, ctx, *, message: str):
        try:
            decoded = base64.b64decode(message.encode()).decode()
        except:
            decoded = '**Error**: Failed to decode.'
        embed = discord.Embed(
            title='Base64 Decode',
            description=decoded
        )
        await editMSG(ctx, embed)
def setup(client):
    client.add_cog(Text(client))
