# bot.py
import os
import discord

from discord.ext import commands
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='<')

#slashes will need to change based on os used
scriptPath = os.path.dirname(os.path.realpath(__file__))
templatePath = os.path.join(scriptPath, 'templates')


@bot.command(name='city17')
@commands.cooldown(1, 1, type=commands.BucketType.user)
async def City_Seventeen(ctx):
    
    lastDiscordImage = await Get_Last_Picture(ctx)
    print(scriptPath)
    uploadedImage = Image.open(os.path.join(scriptPath, lastDiscordImage)).convert("RGBA")
    
    city17Base = Image.open(os.path.join(templatePath, 'city17Background.png'))
    imageMask = Image.open(os.path.join(templatePath, 'City17Mask.png')).convert("L").resize((154, 292))
    wiresOverlap = Image.open(os.path.join(templatePath, 'wires.png')).convert("RGBA")

    #resize image
    uploadedImage = uploadedImage.resize((154, 292))

    #apply mask to give top of screen curviture
    uploadedImage.putalpha(imageMask)

    #tilt image
    uploadedImage = uploadedImage.rotate(-10, Image.Resampling.BICUBIC ,expand=True)

    #overlay onto pre-existing city17
    city17Base.paste(uploadedImage, (134, 363), uploadedImage)

    city17Base.paste(wiresOverlap, (0, 0), wiresOverlap)

    city17Base.save(os.path.join(scriptPath, 'city17.png'))
    
    await ctx.send(file=discord.File(os.path.join(scriptPath, 'city17.png')), content='Welcome! Welcome to City 17!') 
    
    os.remove(os.path.join(scriptPath, lastDiscordImage)) 
    
    #await ctx.send(lastDiscordImage)

# Helper function that saves the last image posted in channel
# and returns that images file name    
async def Get_Last_Picture(ctx):
    async for message in ctx.channel.history(limit=None):
        if message.attachments:
            lastDiscordMedia = message.attachments[0]
            if 'image' in lastDiscordMedia.content_type:
                break
                
    print(await lastDiscordMedia.save( os.path.join(scriptPath, lastDiscordMedia.filename)))
    return lastDiscordMedia.filename

    
bot.run(TOKEN)
