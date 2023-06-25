import discord
from discord.ext import commands


class WelcomeLeave(commands.Cog):
    def __init__(self, client):
        self.client = client

    def get_welcome_channel(self, guild):
        welcome_channel = discord.utils.get(guild.text_channels, name='join-left')
        return welcome_channel

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_channel = self.get_welcome_channel(member.guild)
        if welcome_channel:
            welcome_message = f"Welcome, {member.mention}, to the server! We hope you enjoy your stay."
            await welcome_channel.send(welcome_message)
        else:
            welcome_channel = await self.create_welcome_channel(member.guild)
            if welcome_channel:
                welcome_message = f"Welcome, {member.mention}, to the server! We hope you enjoy your stay."
                await welcome_channel.send(welcome_message)

        community_role = discord.utils.get(member.guild.roles, name="Community 🌟")
        if not community_role:
            community_role = await member.guild.create_role(name="Community 🌟", color=discord.Color.blue(), hoist=True)

        await member.add_roles(community_role)

    async def create_welcome_channel(self, guild):
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=True)
        }
        try:
            welcome_channel = await guild.create_text_channel('join-left', overwrites=overwrites)
            return welcome_channel
        except discord.Forbidden:
            return None

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        welcome_channel = self.get_welcome_channel(member.guild)
        if welcome_channel:
            farewell_message = f"Goodbye, {member.name}! We'll miss you."
            await welcome_channel.send(farewell_message)


async def setup(client):
    await client.add_cog(WelcomeLeave(client))
