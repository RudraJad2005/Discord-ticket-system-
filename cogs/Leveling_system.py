import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import random


class Leveling(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        author = message.author
        guild = message.guild
        async with self.client.db.cursor() as cursor:
            await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?", (author.id, guild.id))
            xp = await cursor.fetchone()
            await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?", (author.id, guild.id))
            level = await cursor.fetchone()

            if not xp or not level:
                await cursor.execute("INSERT INTO levels (xp, level, user, guild) VALUES (?, ?, ?, ?)", (0, 0, author.id, guild.id))
                await self.client.db.commit()

            try:
                xp = xp[0]
                level= level[0]
            except TypeError:
                xp = 0
                level = 0
            if level < 5:
                xp += random.randint(1, 3)
                await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (xp, author.id, guild.id))
            else:
                rand = random.randint(1, (level//4))
                if rand == 1:
                    xp += random.randint(1, 3)
                    await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (xp, author.id, guild.id))
            if xp >= 100:
                level += 1
                await cursor.execute("UPDATE levels SET level = ? WHERE user = ? AND guild = ?", (level, author.id, guild.id))
                await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (0, author.id, guild.id))
                await message.channel.send(f"{author.mention} has leveled up to level **{level}**!")

                # Add role to the member who leveled up
                level_roles = {
                    1: "Level 1",
                    2: "Level 2",
                    3: "Level 3",
                    5: "Level 5",
                    10: "Level 10",
                    15: "Level 15",
                    20: "Level 20",
                    30: "Level 30",
                    40: "Level 40",
                    50: "Level 50",
                    60: "Level 60",
                    70: "Level 70",
                    80: "Level 80",
                    90: "Level 90",
                    100: "Level 100"
                }

                for role_level, role_name in level_roles.items():
                    if level == role_level:
                        role = discord.utils.get(guild.roles, name=role_name)
                        if not role:
                            role = await guild.create_role(name=role_name)
                        await author.add_roles(role)
                        

        await self.client.db.commit()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def level(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        async with self.client.db.cursor() as cursor:
            await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?", (member.id, ctx.guild.id))
            xp = await cursor.fetchone()
            await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?", (member.id, ctx.guild.id))
            level = await cursor.fetchone()

            if not xp or not level:
                await cursor.execute("INSERT INTO levels (levels, xp, user, guild) VALUES (?, ?, ?, ?)", (0, 0, member.id, ctx.guild.id))
                await self.client.db.commit()

            try:
                xp = xp[0]
                level = level[0]
            except TypeError:
                xp = 0
                level = 0

        em = discord.Embed(title=f"{member.name}'s level", description=f"Level: **{level}**\nXP: **{xp}**")
        await ctx.send(embed=em)

    
async def setup(client):
    await client.add_cog(Leveling(client))
