import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import instaloader
import glob


# https://www.youtube.com/watch?v=YD_N6Ffoojw

#------------------
load_dotenv()
token = os.environ['DISCORD_TOKEN']
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='~', intents=intents)
loader = instaloader.Instaloader(dirname_pattern="/usr/local/app")
def downloadFunction(str):
    shortcode = str.split("/")[-2]
    try:
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        loader.download_post(post, target=".")
        filename_base = loader.format_filename(post)
        # Check for video or image file
        for ext in [".mp4", ".jpg"]:
            file_withExt = filename_base + ext
            if os.path.exists(file_withExt):
                return file_withExt
        return None
    except Exception as e:
        return None
    
def removeFunction(str):
    print("HALLLOOOOO :DDDDD %s",str)
    try:
        file_list = glob.glob(str.split(".")[0]+".*")
        print(file_list)
        for file in file_list:
            os.unlink("/usr/local/app/"+file)
            logging.debug("Deleted file %s", str)
            print("Deleted file %s", str)
    except Exception as e:
        logging.error("Unable to delete file: %s", str)
        print("Unable to delete file:%s with exception:%s", str, e)


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
            except discord.HTTPException as e:
                splitMsg = message.content.split("https://www.instagram.com/")[1]
                reply = "https://www.vxinstagram.com/"+splitMsg
                await message.reply("Upload failed, attempting to embed it: "+reply)
                logging.error("Failed to upload file:%s",file2)   
        else:
            splitMsg = message.content.split("https://www.instagram.com/")[1]
            reply = "https://www.vxinstagram.com/"+splitMsg
            await message.reply("Upload failed, attempting to embed it: "+reply)
            logging.error("Failed to upload file:%s",file2) 
    await bot.process_commands(message)
    removeFunction(file2)


bot.run(token, log_handler=handler, log_level=logging.DEBUG)



