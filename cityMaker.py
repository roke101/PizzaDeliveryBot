from PIL import Image

City17Base = Image.open(r'C:\Users\mille\OneDrive\Desktop\discordBot\templates\city17Background.png')
UploadedImage = Image.open(r'C:\Users\mille\OneDrive\Desktop\discordBot\city17.png').convert("RGBA")
ImageMask = Image.open(r'C:\Users\mille\OneDrive\Desktop\discordBot\City17Mask.png').convert("L").resize((154, 292))
wiresOverlap = Image.open(r'C:\Users\mille\OneDrive\Desktop\discordBot\wires.png').convert("RGBA")

#resize image
UploadedImage = UploadedImage.resize((154, 292))

#apply mask to give top of screen curviture
UploadedImage.putalpha(ImageMask)

#tilt image
UploadedImage = UploadedImage.rotate(-10, Image.Resampling.BICUBIC ,expand=True)

#overlay onto pre-existing city17
City17Base.paste(UploadedImage, (134, 363), UploadedImage)

City17Base.paste(wiresOverlap, (0, 0), wiresOverlap)

City17Base.save(r'C:\Users\mille\OneDrive\Desktop\discordBot\city17.png')
