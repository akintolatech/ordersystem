"""
Source: Computer Vision
Desc: Image Conversion
All rights reserved Akintola Technologies  - updt Aug 24
"""

from PIL import Image

# open image
icon = Image.open("buka.png")
# print(icon)


#save in another format
icon.save("est.ico")
