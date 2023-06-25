import discord
from discord.ext import commands
import json
from discord.ext.commands import cooldown, BucketType

class ModLeveling(commands.Cog):
    def __init__(self, client):
        self.client = client
    

    @commands.Cog.listener()
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Try again after {round(error.retry_after, 2)}" , delete_after=2)
    
    def get_modlog_channel(self, guild):
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

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith('+kick'):
            if message.author.guild_permissions.kick_members:
                member = message.mentions[0]
                reason = message.content.split(' ', 2)[2]
                await member.kick(reason=reason)
                await message.channel.send(f'{member.mention} has been kicked.')

            # Find or create the modlog channel
                modlogs_channel = self.get_modlog_channel(message.guild)

            # Send the modlogs embed
                embed = discord.Embed(title='<:RIGHT:1118951528456265768> Member Kicked', color=discord.Color.red())
                embed.add_field(name='Kicked Member', value=member.mention, inline=False)
                embed.add_field(name='Reason', value=reason, inline=False)
                embed.set_footer(text=f'Kicked by {message.author.name}')
                await modlogs_channel.send(embed=embed)
            else:
                await message.channel.send("You don't have permission to kick members.")
        if message.content.startswith('+ban'):
            if message.author.guild_permissions.ban_members:
                member = message.mentions[0]
                reason = message.content.split(' ', 2)[2]
                await member.kick(reason=reason)
                await message.channel.send(f'{member.mention} has been Banned.')

            # Find or create the modlog channel
                modlogs_channel = self.get_modlog_channel(message.guild)
    
            # Send the modlogs embed
                embed = discord.Embed(title='Member Banned', color=discord.Color.red())
                embed.add_field(name='Banned Member', value=member.mention, inline=False)
                embed.add_field(name='Reason', value=reason, inline=False)
                embed.set_footer(text=f'Banned by {message.author.name}')
                await modlogs_channel.send(embed=embed)
            else:
                await message.channel.send("You don't have permission to ban members.")

        if "https" in message.content and len(message.content) > 4:
            await message.delete()
            await message.channel.send(f"{message.author.mention} You cant send links here", delete_after=2)

        if message.author == self.client.user:  # Ignore messages sent by the bot itself
            return

        await self.client.process_commands(message)

async def setup(client):
    await client.add_cog(ModLeveling(client))