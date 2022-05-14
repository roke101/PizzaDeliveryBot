# bot.py
import os
import discord

from discord.ext import commands
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='<')


@bot.command(name='city17')
async def nine_nine(ctx):
    async for message in ctx.channel.history(limit=None):
        if message.attachments:
            media = message.attachments[0]
            if 'image' in media.content_type:
                break
                
    #slashes will need to change based on os used            
    scriptPath = os.path.dirname(os.path.realpath(__file__)) + '\\'
    templatePath = scriptPath + 'templates\\'

    
    print(await media.save( scriptPath + media.filename))
    
    UploadedImage = Image.open(scriptPath + media.filename).convert("RGBA")
    
    City17Base = Image.open(templatePath + 'city17Background.png')
    ImageMask = Image.open(templatePath + 'City17Mask.png').convert("L").resize((154, 292))
    wiresOverlap = Image.open(templatePath + 'wires.png').convert("RGBA")

    #resize image
    UploadedImage = UploadedImage.resize((154, 292))

    #apply mask to give top of screen curviture
    UploadedImage.putalpha(ImageMask)

    #tilt image
    UploadedImage = UploadedImage.rotate(-10, Image.Resampling.BICUBIC ,expand=True)

    #overlay onto pre-existing city17
    City17Base.paste(UploadedImage, (134, 363), UploadedImage)

    City17Base.paste(wiresOverlap, (0, 0), wiresOverlap)

    City17Base.save(scriptPath + 'city17.png')
    
    await ctx.send(file=discord.File(scriptPath + 'city17.png'), content='Welcome! Welcome to City 17!')
    
    os.remove(scriptPath +  media.filename)
    
    #await ctx.send(media)
    
bot.run(TOKEN)
