# Import necessary libraries and modules
import math
import discord
from discord import Intents, app_commands
from discord.ext import commands, tasks
from itertools import cycle
import os
import aiosqlite
import asyncio
from dotenv import load_dotenv
import leveling

# Define the intents the bot needs
intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intents
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
client.multiplier = 1  # Set a multiplier for leveling

# Load bot token from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Async function to initialize the bot
async def initialise():
    client.db = await aiosqlite.connect("expdata.db")
    await client.db.execute(
        "CREATE TABLE IF NOT EXISTS guildData (guild_id int, user_id int, exp int, PRIMARY KEY (guild_id, user_id))"
    )

# Event handler for when the bot is ready
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Streaming(name='Follow PoMalaW on twitch (he may be coding on stream)', url='https://www.twitch.tv/pomalaw'))
    print(f"{client.user} is now running")
    # Use client.loop.create_task to run the async function within the on_ready event
    await initialise()

# Event handler for when a message is received
@client.event
async def on_message(message):
    if message.author.bot:
        return

    # Check if the content of the message is "Hello"
    if message.content == "Hello":
        await message.channel.send("Hey sweetie :3")

    # command to sync the / commands
    if message.content == "!sync":
        await tree.sync()
        await message.reply(f"synced commands")

    # Call the leveling function passing 'client' and 'message'
    await leveling.handle_leveling(client, message)

# Command to display user stats
@tree.command(name="stats", description="Show user stats")
async def stats(interaction, member: discord.Member = None):
    if member is None:
        member = interaction.user

    # Get user XP
    async with client.db.execute(
        "SELECT exp FROM guildData WHERE guild_id = ? and user_id = ?",
        (interaction.guild.id, member.id),
    ) as cursor:
        data = await cursor.fetchone()
        if data:
            exp = data[0]
        else:
            # Handle the case where no data is found for the member
            await interaction.response.send_message(
                "No data found for the specified member."
            )
            return

    # Calculate rank and level progress
    async with client.db.execute(
        "SELECT exp FROM guildData WHERE guild_id = ?", (interaction.guild.id,)
    ) as cursor:
        rank = 1
        async for value in cursor:
            if exp < value[0]:
                rank += 1

    lvl = int(math.sqrt(exp) // client.multiplier)

    current_lvl_exp = (client.multiplier * (lvl)) ** 2
    next_lvl_exp = (client.multiplier * ((lvl + 1))) ** 2

    lvl_percentage = ((exp - current_lvl_exp) / (next_lvl_exp - current_lvl_exp)) * 100

    # Create and send an embed with user stats
    embed = discord.Embed(
        title=f"Stats for {member.name}", colour=discord.Colour.gold()
    )
    embed.add_field(name="Level", value=str(lvl))
    embed.add_field(name="Exp", value=f"{exp}/{next_lvl_exp}")
    embed.add_field(name="Rank", value=f"{rank}/{interaction.guild.member_count}")
    embed.add_field(name="Level Progress", value=f"{round(lvl_percentage, 2)}%")

    await interaction.response.send_message(content="", embed=embed)

# Command to display a leaderboard with pagination buttons
@tree.command(name="ping", description="Show the ping of the server")
async def ping(message):
    bot_latency = round(client.latency * 1000)
    await message.channel.send(f"Pong ! {bot_latency} ms.")

# Start the bot by creating a task for initialization and running it
client.run(DISCORD_TOKEN)