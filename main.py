import discord
from discord.ext import commands
import asyncio
from datetime import timedelta
import datetime
import discord.ui
from discord.ui import View, Button, Select
import aiosqlite
import json
import os
import aiohttp
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

intents = discord.Intents.all()
intents.messages = True
intents.guilds = True
intents.reactions = True
intents.members = True
# intents.message_components = True
client = commands.Bot(command_prefix='+', intents=intents)



@client.event
async def on_ready():
    print("Bot is ready")
    await client.tree.sync()
    setattr(client, "db", await aiosqlite.connect("level.db"))
    await asyncio.sleep(3)
    async with client.db.cursor() as cursor:
        await cursor.execute("CREATE TABLE IF NOT EXISTS levels (level INTEGER, xp INTEGER, user INTEGER, guild INTEGER)")


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')


# Set up the SQLAlchemy engine and session
engine = create_engine('sqlite:///guild_data.db')
Session = sessionmaker(bind=engine)
session = Session()
initial_extensions = ['cogs.ticket_system']

if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)

def get_modlog_channel(guild):
    # Check if the modlog channel exists
    modlogs_channel = discord.utils.get(guild.text_channels, name='modlogs')
    if modlogs_channel is not None:
        return modlogs_channel

    # If the modlog channel doesn't exist, create a new one
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True)
    }
    return guild.create_text_channel('modlogs', overwrites=overwrites)



#CoolDown command

@client.event
async def on_command_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.CommandOnCooldown):
        await interaction.response.send_message(f"Try again after {round(error.retry_after, 2)}" , delete_after=2)

# @client.command()
# async def invite(ctx: commands.Context):
#     inv = await ctx.channel.create_invite()
#     await ctx.send("Click the below button", view=InviteButtons(str(inv)))

@client.event
async def on_button_click(interaction):
    if interaction.component.custom_id == 'ticket_button':
        await interaction.respond(type=discord.InteractionType.ChannelMessageWithSource, content='Button clicked!')

@client.tree.command(name="ping", description="gives ur ping")
async def ping(interaction: discord.Interaction):
    latency = round(client.latency * 1000)  # Calculates the bot's latency in milliseconds
    await interaction.response.send_message(f'Pong! My current ping is {latency}ms.')


@client.tree.command(name="length", description="gives length of ur line")
@commands.cooldown(1, 5, commands.BucketType.user)
async def length(interaction: discord.Interaction):
    user_input = interaction.data['options'][0]['value']
    await interaction.response.send_message(f'Your message is {len(user_input)} characters long.')

async def main():
    await load()
    # await client.start("ODkyMzI0MDAxOTM2OTgyMDY3.GJ0MO_.mGo3YX9ZrBtp4MmxkSNY9lS9pzyP_4X9r41dEY")
    await client.start("MTEwMTkxOTM3MjM0MTE2MjAwNA.Gf0fUV.zANWSSfVaZZ-Cf8-9xJV4AUQjKDV8OiDA3s2dg")

asyncio.run(main())
