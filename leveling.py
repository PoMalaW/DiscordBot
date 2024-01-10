# Import necessary libraries and modules
import math

# Event handler for when a message is received (leveling system)

async def handle_leveling(client, message):
    if not message.author.bot:
        cursor = await client.db.execute("INSERT OR IGNORE INTO guildData (guild_id, user_id, exp) VALUES (?, ?, ?)", (message.guild.id, message.author.id, 1))
        if cursor.rowcount == 0:
            # Update user's experience points
            await client.db.execute("UPDATE guildData SET exp = exp + 1 WHERE guild_id = ? AND user_id = ?", (message.guild.id, message.author.id))
            # Calculate level and send a message if the user leveled up
            cur = await client.db.execute("SELECT exp FROM guildData WHERE guild_id = ? AND user_id = ?", (message.guild.id, message.author.id))
            data = await cur.fetchone()
            exp = data[0]
            lvl = math.sqrt(exp) / client.multiplier                    
            if lvl.is_integer():
                await message.channel.send(f"{message.author.mention} Well done you are now level : {int(lvl)} !")

    await client.db.commit()