import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import utils
from discord.ext.commands import cooldown, BucketType
import logging
import traceback
import sys
import json

# Configure logging settings
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),  # Save log messages to a file
        logging.StreamHandler()  # Print log messages to the console
    ]
)

# Create a logger
logger = logging.getLogger(__name__)

class ticket_syatem(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.blurple, custom_id="ticket_button")
    async def ticket_system(self, interaction: discord.Interaction, button: discord.ui.Button):
            ticket = utils.get(interaction.guild.text_channels, name=f"ticket-for-{interaction.user.name}-{interaction.user.discriminator}")
            if ticket is not None:
                await interaction.response.send_message(f"You already have a ticket open {ticket.mention}", ephemeral=True)
            else:
                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, embed_links=True),
                    interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
                    }
                channel = await interaction.guild.create_text_channel(
                    name=f"ticket-for-{interaction.user.name}-{interaction.user.discriminator}",
                    overwrites=overwrites,
                    reason=f"Ticket for {interaction.user}"
                )
                await channel.send(f"{interaction.user.mention} Need's help", view=main())
                await interaction.response.send_message(f"I've opened a ticket for you {channel.mention}!", ephemeral=True)
            
        

class TicketSystem(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_button_click(self, interaction: discord.Interaction):
        if interaction.component.custom_id == "close":
            if "ticket-for" in interaction.channel.name:
                embed = discord.Embed(title="Are you sure you want to close this ticket")
                await interaction.response.send_message(embed=embed, view=confirm(), ephemeral=True)
            else:
                await interaction.response.send_message("This isn't a ticket", ephemeral=True)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    async def ticket(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Ticket System", description="Click the button below to create a ticket.")
        await interaction.channel.send(embed=embed, view=ticket_syatem())
        await interaction.response.send_message("Ticket system is opned", ephemeral=True)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    async def close(self, interaction: discord.Interaction):
        if "ticket-for" in interaction.channel.name:
            embed = discord.Embed(title="Are you sure you want to close this ticket")
            await interaction.response.send_message(embed=embed, view=confirm(), ephemeral=True)
        else:
            await interaction.response.send_message("This isn't a ticket", ephemeral=True)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    async def adduser(self, interaction: discord.Interaction, user: discord.Member):
        if "ticket-for" in interaction.channel.name:
            await interaction.channel.set_permissions(
                user,
                view_channel=True,
                send_messages=True,
                attach_files=True,
                embed_links=True
            )
            await interaction.response.send_message(
                f"{user.mention} has been added to the ticket by {interaction.user.mention}"
            )
        else:
            await interaction.response.send_message("This isn't a ticket", ephemeral=True)

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.", delete_after=2)
        else:
            print(f"Ignoring exception in command {ctx.command}:", file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


class confirm(View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.red, custom_id="confirm")
    async def confirm_button(self, interaction, button):
        try:
            await interaction.channel.delete()
        except:
            await interaction.response.send_message(
                "Channel deleted! Make sure I have `manage_channel` permissions!",
                ephemeral=True
            )


class main(View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red, custom_id="close")
    async def close(self, interaction, button):
        embed = discord.Embed(title="Are you sure to close ticket", color=discord.Colour.red())
        await interaction.response.send_message(embed=embed, view=confirm(), ephemeral=True)


async def setup(client):
    await client.add_cog(TicketSystem(client))
    client.add_listener(TicketSystem(client).on_button_click)
