import requests
from PIL import Image

url  = 'https://cdn.discordapp.com/emojis/587726828815384738.png?v=1'


im = Image.open(requests.get(url, stream=True).raw)
im.show()
print(type(im))