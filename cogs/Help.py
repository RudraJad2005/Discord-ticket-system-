import discord
from discord.ext import commands


class InviteButtons(discord.ui.View):
    def __init__(self, inv: str):
        super().__init__()
        self.inv = inv
        self.add_item(discord.ui.Button(label="Invite link", url="https://discord.com/api/oauth2/authorize?client_id=892324001936982067&permissions=8&scope=bot"))

class HelpCommand(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:  # Ignore messages sent by bots
            return

        if before.content == after.content:  # Ignore edits that don't change the content
            return

    # Find or create the modlogs channel
        modlogs_channel = self.get_modlog_channel(before.guild)

    # Send the edited message in an embed to the modlogs channel
        embed = discord.Embed(title="Message Edited", color=discord.Color.orange())
        embed.add_field(name="Author", value=before.author.mention, inline=False)
        embed.add_field(name="Before", value=before.content, inline=False)
        embed.add_field(name="After", value=after.content, inline=False)
        embed.set_footer(text=f"Channel: #{before.channel.name}")
        await modlogs_channel.send(embed=embed)


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx: commands.Context):
        inv = await ctx.channel.create_invite()
        embed = discord.Embed(title="Team Nexus Artemis [nXa]", description="Join our server [Team Nexus Artemis](https://discord.gg/kX6zjzB2vb)", color=discord.Color.green())
        embed.add_field(name="Commands List", value="```ticket``` ```kick``` ```ban``` ```mute``` ```unmute``` ```ping``` ```invite``` ```roster``` ```createchannel``` ```deletechannel``` ```mute``` ```unmute``` ```warn``` ```showwarns``` ```clearwarns```", inline=True)
        await ctx.send(embed=embed, view=InviteButtons(str(inv)))

async def setup(client):
    if client.get_command('help'):
        client.remove_command('help')
    await client.add_cog(HelpCommand(client))
