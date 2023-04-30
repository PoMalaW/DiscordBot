import nextcord
from nextcord.ext import commands

client = nextcord.Client()

@client.event
async def on_ready():
    print(f"{client.user} is now running")

with open("token.txt", "r") as file:
    token = file.readline()

client.run(token)