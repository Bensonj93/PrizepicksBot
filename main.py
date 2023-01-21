
import discord
from discord.ext import commands
import json
import os


intents = discord.Intents.default()
intents.members= True
intents.message_content = True

bot = commands.Bot(command_prefix="?", intents = intents)

bot.remove_command("help")

if __name__ == "__main__":
    for filename in os.listdir("Cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"Cogs.{filename[:-3]}")


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    print(discord.__version__)


#--------------------------------RUN---------------#
with open("config.json", 'r') as config:
    data = json.load(config)
    token = data["token"]

bot.run(token)

