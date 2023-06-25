import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

muted_members = []

class Mute(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, duration: int, unit: str):
        muted_role = discord.utils.get(ctx.guild.roles, name='Muted')

        if not muted_role:
        # Create muted role if it doesn't exist
            muted_role = await ctx.guild.create_role(name='Muted')
    
        # Set permissions for the muted role
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, speak=False, send_messages=False)

        if muted_role in member.roles:
            await ctx.send(f'{member.mention} is already muted.')
            return

    # Calculate the duration in seconds based on the specified unit
        if unit.lower() == 'seconds':
            duration_seconds = duration
        elif unit.lower() == 'minutes':
            duration_seconds = duration * 60
        elif unit.lower() == 'hours':
            duration_seconds = duration * 60 * 60
        elif unit.lower() == 'days':
            duration_seconds = duration * 24 * 60 * 60
        elif unit.lower() == 'weeks':
            duration_seconds = duration * 7 * 24 * 60 * 60
        else:
            await ctx.send('Invalid unit. Please specify seconds, minutes, hours, days, or weeks.')
            return

    # Add the muted role to the member
        await member.add_roles(muted_role)
        muted_members.append(member.id)

        embed = discord.Embed(title="Muted", description=f"{member.mention} got muted for {duration} {unit}", color=discord.Color.yellow())
        modlog_channel = self.get_modlog_channel(ctx.guild)
        await modlog_channel.send(embed=embed)
        await ctx.send(embed=embed)

    # Wait for the specified duration and then unmute the member
        await self.asyncio.sleep(duration_seconds)
        if member.id in muted_members:
            await member.remove_roles(muted_role)
            muted_members.remove(member.id)
            unmute_embed = discord.Embed(title="Unmuted", description=f"{member.mention} has been unmuted.", color=discord.Color.green())
            await modlog_channel.send(embed=unmute_embed)

@commands.command()
@commands.has_permissions(manage_roles=True)
async def unmute(self, ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name='Muted')

    if muted_role in member.roles:
        await member.remove_roles(muted_role)
        muted_members.remove(member.id)
        embed = discord.Embed(title="Unmuted", description=f"{member.mention} has been manually unmuted.", color=discord.Color.green())
        modlog_channel = self.get_modlog_channel(ctx.guild)
        await modlog_channel.send(embed=embed)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f'{member.mention} is not muted.')

async def setup(client):
    await client.add_cog(Mute(client))