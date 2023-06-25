import discord
from discord.ext import commands



class Purge(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name="purge", description="Purge a specified number of messages")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        if amount <= 0:
            await ctx.send("Please provide a positive number of messages to purge.")
            return

        await ctx.channel.purge(limit=amount + 1)  # +1 to include the purge command itself

        embed = discord.Embed(
            title="Message Purge",
            description=f"{amount} messages purged in {ctx.channel.mention}",
            color=discord.Color.red()
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

        await ctx.send(f"{amount} messages have been deleted")
        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Purge(client))
