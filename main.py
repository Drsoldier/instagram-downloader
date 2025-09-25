import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import instaloader


# https://www.youtube.com/watch?v=YD_N6Ffoojw
# https://sssinstagram.com/

#------------------
def remove_utc_files():
    for file in os.listdir("."):
        if "UTC" in file:
            try:
                os.remove(file)
            except Exception as e:
                print(f"Could not remove {file}: {e}")
#------------------
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!shit', intents=intents)
loader = instaloader.Instaloader(dirname_pattern=".")
def test(str):
    shortcode = str.split("/")[-2]
    post = instaloader.Post.from_shortcode(loader.context, shortcode)
    loader.download_post(post, target=".")
    filename_base = loader.format_filename(post)
    # Check for video or image file
    for ext in [".mp4", ".jpg"]:
        file_path = filename_base + ext
        if os.path.exists(file_path):
            return file_path
    return None
    

@bot.event
async def on_ready():
    print("A")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "https://www.instagram.com/" in message.content.lower():
        file2 = test(message.content.strip())
        end = file2.split(".")[1]
        await message.channel.send(file=discord.File(os.getcwd()+"/"+file2, filename="video."+end))
        if os.path.exists(file2):
            os.remove(file2)
            remove_utc_files()

    await bot.process_commands(message)


bot.run(token, log_handler=handler, log_level=logging.DEBUG)



