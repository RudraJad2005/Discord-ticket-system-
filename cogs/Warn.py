import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

warnings = {}


class ModLeveling(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Handle the error
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"This command is on cooldown. Please try again in {error.retry_after:.2f} seconds.")

class WarnCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Handle the error
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide all the required arguments for the command.")


class WarnCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Try again after {round(error.retry_after, 2)}" , delete_after=2)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, BucketType.user)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        if member.id not in warnings:
            warnings[member.id] = {"count": 0, "reasons": []}
        
        warnings[member.id]["count"] += 1
        warnings[member.id]["reasons"].append(reason)
    
        await ctx.send(f"{member.mention} has been warned. Total warnings: {warnings[member.id]['count']}")
    
        if warnings[member.id]["count"] >= 3:
            await ctx.guild.ban(member, reason="Exceeded warning limit.")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, BucketType.user)
    async def clearwarns(self, ctx, member: discord.Member):
        if member.id in warnings:
            warnings.pop(member.id)
            await ctx.send(f"All warnings for **{member.mention}** have been cleared.")
        else:
            await ctx.send("No warnings found for the member.")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, BucketType.user)
    async def showwarns(self, ctx, member: discord.Member):
        if member.id in warnings:
            embed = discord.Embed(title="Warnings", description=f"Warnings for {member.mention}", color=discord.Color.gold())

            for i, reason in enumerate(warnings[member.id]["reasons"], start=1):
                embed.add_field(name=f"Warning {i}", value=reason or "No reason provided", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("No warnings found for the member.")
    
    @warn.error
    @showwarns.error
    @clearwarns.error
    async def warn_showwarns_clearwarns(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")

async def setup(client):
    await client.add_cog(WarnCommand(client))
