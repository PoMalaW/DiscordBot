# Import necessary libraries and modules
import math
import discord
from discord.ext import commands

# Event handler for when a message is received (leveling system)

async def handle_leveling(client, message):
    if not message.author.bot:
        cursor = await client.db.execute("INSERT OR IGNORE INTO guildData (guild_id, user_id, exp) VALUES (?, ?, ?)", (message.guild.id, message.author.id, 1))
        if cursor.rowcount == 0:
            member = message.author
            # Update user's experience points
            await client.db.execute("UPDATE guildData SET exp = exp + 1 WHERE guild_id = ? AND user_id = ?", (message.guild.id, message.author.id))
            # Calculate level and send a message if the user leveled up
            cur = await client.db.execute("SELECT exp FROM guildData WHERE guild_id = ? AND user_id = ?", (message.guild.id, message.author.id))
            data = await cur.fetchone()
            exp = data[0]
            lvl = math.sqrt(exp) / client.multiplier                    
            if lvl.is_integer():
                await message.channel.send(f"{message.author.mention} Well done you are now level : {int(lvl)} !")
            await level_role(member,lvl)

    await client.db.commit()

#asign role to member for level bearing
async def level_role(member, lvl):
    with open("rank_level.txt", "r") as f:
        if lvl == 5:
            role = f.readlines(1)
            await member.add_roles(member,role)
        if lvl % 10 == 0:
            role = f.readlines((lvl / 10) + 1)
            await member.add_roles(member, role)