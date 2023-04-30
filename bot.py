import nextcord
from nextcord.ext import commands

client = nextcord.Client()
guild_ID = 1102207262057037886

@client.event
async def on_ready():
    print(f"{client.user} is now running")

with open("token.txt", "r") as file:
    token = file.readline()

@client.slash_command(description="My first slash command", guild_ids=[guild_ID])
async def kebab(interaction: nextcord.Interaction):
    await interaction.send("Hello !")

client.run(token)