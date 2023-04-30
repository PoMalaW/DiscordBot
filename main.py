import discord

client = discord.Bot(intents=discord.Intents.all())

@client.event
async def on_ready():
    print("[INFO] Bot is ready !")

client.run(open("token.txt", "r").readline())