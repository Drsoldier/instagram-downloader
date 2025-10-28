import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import instaloader


# https://www.youtube.com/watch?v=YD_N6Ffoojw

#------------------
def remove_utc_files():
    for file in os.listdir("."):
        if "UTC" in file:
            try:
                if ".mp4" not in file:
                    os.remove(file)
            except Exception as e:
                print(f"Could not remove {file}: {e}")
#------------------
load_dotenv()
token = os.environ['DISCORD_TOKEN']
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='~', intents=intents)
loader = instaloader.Instaloader(dirname_pattern=".")
def downloadFunction(str):
    shortcode = str.split("/")[-2]
    try:
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        loader.download_post(post, target=".")
        filename_base = loader.format_filename(post)
        # Check for video or image file
        for ext in [".mp4", ".jpg"]:
            file_path = filename_base + ext
            if os.path.exists(file_path):
                return file_path
        return None
    except Exception as e:
        return None
    

@bot.event
async def on_ready():
    print("A")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "https://www.instagram.com/" in message.content.lower():
        file2 = downloadFunction(message.content.strip())
        if file2 is not None:
            try:
                end = file2.split(".")[1]
                test = await message.reply(file=discord.File(os.getcwd()+"/"+file2, filename="video."+end))
                remove_utc_files()
            except discord.HTTPException as e:
                splitMsg = message.content.split("https://www.instagram.com/")[1]
                reply = "https://www.vxinstagram.com/"+splitMsg
                await message.reply("Upload failed, attempting to embed it: "+reply)
                logging.error("Failed to upload file:%s",file2)
            if os.path.exists(file2):
                os.remove(file2)    
        else:
            splitMsg = message.content.split("https://www.instagram.com/")[1]
            reply = "https://www.vxinstagram.com/"+splitMsg
            await message.reply("Upload failed, attempting to embed it: "+reply)
            logging.error("Failed to upload file:%s",file2) 
    await bot.process_commands(message)


bot.run(token, log_handler=handler, log_level=logging.DEBUG)



