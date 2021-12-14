import discord
from discord.ext import commands
from PIL import Image, ImageSequence
import requests
from io import BytesIO

url = 'https://cdn.discordapp.com/avatars/380049846356279296/818ceb5ec31831d81d1caa9402fd3400.webp?size=1024'
response = requests.get(url).content
background = Image.open(BytesIO(response))
background = background.resize((498,280))
animated_gif  = Image.open('/home/pi/discordbot/static/gifs/communism.gif')

background.info['transparency'] = 0.5

background.save('GIF.gif')