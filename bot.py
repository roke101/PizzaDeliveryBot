# bot.py
import os
import time
import discord

from discord.ext import commands
from dotenv import load_dotenv
from PIL import Image

from pytube import YouTube
import cv2
import numpy as np
import moviepy.editor as mpe

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='<', activity=discord.Game(name="Pizza Ya San"))

scriptPath = os.path.dirname(os.path.realpath(__file__))
templatePath = os.path.join(scriptPath, 'templates')

# the section bellow handles storing pictures on the server
# this  feautre is disabled by default and is set in .env
# SAVE_PICTURE_PERMENANTLY needs to be set to true and
# SAVE_PICTURE_ID_WHITELIST needs to contain the server id the bot is saving pictures from
savePicturePermenantly = os.getenv('SAVE_PICTURE_PERMENANTLY', default='False')
savePictureIdWhitelist = os.getenv('SAVE_PICTURE_ID_WHITELIST', default="").split(",")

#save picture path is optional, by default it saves pictures in the script directory
savePicturePath = os.getenv('SAVE_PICTURE_PATH', default=scriptPath)




@bot.command(name='city17')
@commands.cooldown(1, 1, type=commands.BucketType.user)
async def City_Seventeen(ctx):
    
    lastDiscordImage = await Get_Last_Picture(ctx)
    uploadedImage = Image.open(os.path.join(scriptPath, lastDiscordImage)).convert("RGBA")
    
    city17Base = Image.open(os.path.join(templatePath, 'city17Template.png'))
    imageMask = Image.open(os.path.join(templatePath, 'City17Mask.png')).convert("L").resize((154, 292))
    wiresOverlap = Image.open(os.path.join(templatePath, 'wiresTemplate.png')).convert("RGBA")

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
    
    Save_Generated_Picture(ctx, city17Base)
    
@bot.command(name='grind')
@commands.cooldown(1, 1, type=commands.BucketType.user)
async def Grind(ctx):
    
    lastDiscordImage = await Get_Last_Picture(ctx)
    uploadedImage = Image.open(os.path.join(scriptPath, lastDiscordImage)).convert("RGBA")

    grindBase = Image.open(os.path.join(templatePath, 'grindTemplate.png'))

    #resize image
    uploadedImage = uploadedImage.resize(grindBase.size)
    
    #calculate and apply new scaling and position to the base image
    width = uploadedImage.size[0]
    height = uploadedImage.size[1]
    widthRescaled = int(uploadedImage.size[0] * 1.1)
    heightRescaled = int(uploadedImage.size[1] * 1.298)
    #put the image in the center of the canvas with some displacement
    widthRepositioned = (widthRescaled - width)//2 + 2
    heightRepositioned = (heightRescaled - height)//2 - 23
    
    #scale and paste uploaded image onto a black background
    canvas = Image.new("RGBA", (widthRescaled, heightRescaled))
    canvas.paste(uploadedImage, (widthRepositioned, heightRepositioned))
    uploadedImage = canvas
    uploadedImage = uploadedImage.resize(grindBase.size)

    #paste the grind template over the new scaled and positioned image
    uploadedImage.paste(grindBase, (0, 0), grindBase)

    uploadedImage.save(os.path.join(scriptPath, 'grind.png'))
    
    await ctx.send(file=discord.File(os.path.join(scriptPath, 'grind.png'))) 
    
    os.remove(os.path.join(scriptPath, lastDiscordImage))
    
    Save_Generated_Picture(ctx, uploadedImage)
    
@bot.command(name='walmart')
@commands.cooldown(1, 1, type=commands.BucketType.user)
async def Walmart(ctx):
    
    lastDiscordImage = await Get_Last_Picture(ctx)
    uploadedImage = Image.open(os.path.join(scriptPath, lastDiscordImage)).convert("RGBA")
    
    walmartBase = Image.open(os.path.join(templatePath, 'walmartTemplate.png'))

    #resize image
    uploadedImage = uploadedImage.resize((190, 224))

    #overlay onto walmart template
    walmartBase.paste(uploadedImage, (428, 94), uploadedImage)

    walmartBase.save(os.path.join(scriptPath, 'walmart.png'))
    
    await ctx.send(file=discord.File(os.path.join(scriptPath, 'walmart.png'))) 
    
    os.remove(os.path.join(scriptPath, lastDiscordImage))
    
    Save_Generated_Picture(ctx, walmartBase)
    
@bot.command(name='bobross')
@commands.cooldown(1, 1, type=commands.BucketType.user)
async def Bobross(ctx):
    
    lastDiscordImage = await Get_Last_Picture(ctx)
    uploadedImage = Image.open(os.path.join(scriptPath, lastDiscordImage)).convert("RGBA")
    
    bobRossBase = Image.open(os.path.join(templatePath, 'bobRossTemplate.png'))
    bobRossCopy = bobRossBase.copy()
    #resize image
    uploadedImage = uploadedImage.resize((453, 340))


    #overlay onto bobRoss template
    bobRossBase.paste(uploadedImage, (19, 71), uploadedImage)
    #overlay again since there is no more scaling to be done
    bobRossBase.paste(bobRossCopy, (0, 0), bobRossCopy)

    bobRossBase.save(os.path.join(scriptPath, 'bobross.png'))
    
    await ctx.send(file=discord.File(os.path.join(scriptPath, 'bobross.png'))) 
    
    os.remove(os.path.join(scriptPath, lastDiscordImage))
    
    Save_Generated_Picture(ctx, bobRossBase)
    
@bot.command(name='dominos')
@commands.cooldown(1, 1, type=commands.BucketType.user)
async def Dominos(ctx):
    
    lastDiscordImage = await Get_Last_Picture(ctx)
    uploadedImage = Image.open(os.path.join(scriptPath, lastDiscordImage)).convert("RGBA")
    
    dominosBase = Image.open(os.path.join(templatePath, 'dominosTemplate.png')).convert("RGBA")
    dominosCopy = dominosBase.copy()
    #resize image
    uploadedImage = uploadedImage.resize((103, 173))
    uploadedImage = uploadedImage.rotate(-3.25, Image.Resampling.BICUBIC ,expand=True)

    #overlay onto dominos template
    dominosBase.paste(uploadedImage, (232, 295), uploadedImage)
    dominosBase.paste(dominosCopy, (0, 0), dominosCopy)

    dominosBase.save(os.path.join(scriptPath, 'dominos.png'))
    
    await ctx.send(file=discord.File(os.path.join(scriptPath, 'dominos.png'))) 
    
    os.remove(os.path.join(scriptPath, lastDiscordImage))
    
    Save_Generated_Picture(ctx, dominosBase)
    
@bot.command(name='trump')
@commands.cooldown(1, 1, type=commands.BucketType.user)
async def Trump(ctx):
    
    lastDiscordImage = await Get_Last_Picture(ctx)
    uploadedImage = Image.open(os.path.join(scriptPath, lastDiscordImage)).convert("RGBA")
    
    trumpBase = Image.open(os.path.join(templatePath, 'trumpTemplate.png'))
    trumpCopy = trumpBase.copy()

    uploadedImage = uploadedImage.resize((335, 300))
    uploadedImage = uploadedImage.rotate(4, Image.Resampling.BICUBIC ,expand=True)
    #resize image

    #overlay onto walmart template
    trumpBase.paste(uploadedImage, (87, 80), uploadedImage)
    trumpBase.paste(trumpCopy, (0,0), trumpCopy)

    trumpBase.save(os.path.join(scriptPath, 'trump.png'))
    
    await ctx.send(file=discord.File(os.path.join(scriptPath, 'trump.png'))) 
    
    os.remove(os.path.join(scriptPath, lastDiscordImage))
    
    Save_Generated_Picture(ctx, trumpBase)
    
    
@bot.command(name='greenscreen')
@commands.cooldown(1, 1, type=commands.BucketType.user)
async def Greenscreen(ctx, arg):
    
    lastDiscordImage = await Get_Last_Picture(ctx)
    
    yt = YouTube(arg)

    filter = yt.streams.filter(file_extension="mp4").get_by_resolution("720p")
    if filter.filesize < 8000000:
        filter.download(scriptPath, filename="videoOut.mp4")
    else:
        filter = yt.streams.filter(file_extension="mp4").get_by_resolution('360p')
        if filter.filesize < 8000000:
            filter.download(scriptPath, filename="videoOut.mp4")
        else:
            await ctx.send(content='The video linked is over 8MB, please use another video.')
            return
    
    video = cv2.VideoCapture(os.path.join(scriptPath, "videoOut.mp4"))
    image = cv2.imread(os.path.join(scriptPath, lastDiscordImage))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    fourcc = cv2.VideoWriter_fourcc(*'XVID');
    out = cv2.VideoWriter(os.path.join(scriptPath, 'test_vid.avi'),fourcc, video.get(cv2.CAP_PROP_FPS), (640, 480));

    done = False;
    while not done:

        ret, frame = video.read()
        if not ret:
            done = True;
            continue;
        

        frame = cv2.resize(frame, (640, 480))
        image = cv2.resize(image, (640, 480))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        

        u_green = np.array([89, 255, 255])
        l_green = np.array([36, 50, 70])

        mask = cv2.inRange(frame, l_green, u_green)
        res = cv2.bitwise_and(frame, frame, mask = mask)
        black_pixels = np.where(
        (frame[:, :, 0] == 0) & 
        (frame[:, :, 1] == 0) & 
        (frame[:, :, 2] == 0))
        frame[black_pixels] = [1, 1, 1]

        f = frame - res
        f = np.where(f == 0, image, f)
        f = cv2.cvtColor(f, cv2.COLOR_HSV2BGR)

        #cv2.imshow("video", frame)
        #cv2.imshow("mask", f)

        out.write(f)
        #if cv2.waitKey(25) == 27:
        #    break

    out.release()
    video.release()
    cv2.destroyAllWindows()
    out = None


    videoMPE = mpe.VideoFileClip(os.path.join(scriptPath, "videoOut.mp4"))
    final_audio = videoMPE.audio

    my_clip = mpe.VideoFileClip(os.path.join(scriptPath, "test_vid.avi"))

    my_clip.audio = final_audio
    my_clip.write_videofile(os.path.join(scriptPath, "meme.mp4"))
    
    await ctx.send(file=discord.File(os.path.join(scriptPath, "meme.mp4")))
    
    videoMPE.close()
    my_clip.close()
    
    os.remove(os.path.join(scriptPath, lastDiscordImage))
    os.remove(os.path.join(scriptPath, "videoOut.mp4"))
    os.remove(os.path.join(scriptPath, "test_vid.avi"))
    os.remove(os.path.join(scriptPath, "meme.mp4"))

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

# Helper function that saves the last Generated image permanently
# to the server if the if condition is true  
def Save_Generated_Picture(ctx, saveImage):
    #if save pcitures is set to true and the server sending the message is on the white list
    if(savePicturePermenantly == 'True' and str(ctx.message.guild.id) in savePictureIdWhitelist):
        #get the destination path wed like to write to 
        #formatted *path*\PizzaDeliveryBotSavedPictures\*serverName*\*commandName*
        dest = os.path.join(savePicturePath, 'PizzaDeliveryBotSavedPictures', ctx.message.guild.name.replace(' ', '_'), ctx.command.name)
        #if the directory doesnt exist, make it
        if not os.path.exists(dest):
            os.makedirs(dest)
        list = os.listdir(dest)
        numberOfFiles = len(list)
        #save picture to *path*\PizzaDeliveryBotSavedPictures\*commandName*\*commandNameTotalFilesPlus1.png*
        saveImage.save(os.path.join(dest, ctx.command.name + str(numberOfFiles + 1) + '.png'))
    
bot.run(TOKEN)
 