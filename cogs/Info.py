import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import traceback
import sys

class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    # This command is for info of the server
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def info(self, ctx):
        info_embed = discord.Embed(title=f"Information about {ctx.guild.name}", description="All public information about this server", color=discord.Color.green())
        info_embed.set_thumbnail(url=ctx.guild.icon)
        info_embed.add_field(name="Name", value=ctx.guild.name, inline=False)
        info_embed.add_field(name="ID:", value=ctx.guild.id, inline=False)
        info_embed.add_field(name="Owner", value=ctx.guild.owner, inline=False)
        info_embed.add_field(name="Member count", value=ctx.guild.member_count, inline=False)
        info_embed.add_field(name="Channel count", value=len(ctx.guild.channels), inline=False)
        info_embed.add_field(name="Role count", value=len(ctx.guild.roles), inline=False)
        info_embed.add_field(name="Rules count", value=ctx.guild.rules_channel, inline=False)
        info_embed.add_field(name="Booster count", value=ctx.guild.premium_subscription_count, inline=False)
        info_embed.add_field(name="Booster Tire", value=ctx.guild.premium_subscriber_role, inline=False)
        info_embed.add_field(name="Created AT", value=ctx.guild.created_at.__format__("%A, %d, %B %Y @ %H:%M:%S"), inline=False)
        info_embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar)

        await ctx.send(embed=info_embed)

    # Error handling
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.", delete_after=2)
        else:
            print(f"Ignoring exception in command {ctx.command}:", file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

async def setup(client):
    await client.add_cog(Info(client))
