#!/usr/bin/python3

import sys, random
from PIL import Image, ImageDraw

pixelsPerFrame = 8; outputFile = "output.gif"
imageSize = (400, 200); imageColor = "#000000"
pixelColors = ["#ff0000", "#00ff00", "#0000ff", "#000000"]

for argument in sys.argv:
    argument = argument.lower()
    if argument == "help":
        print("""arguments:
size - dimensions of the output image
speed - pixels drawn per frame
start - color of the base image
colors - list of colors to be used
output - path of the output image

example:
pixelgenerator size:400x200 start:#0068DB speed:16 colors:#FF0000,#00FF00 output:file.gif"""); exit()
    elif argument.startswith("size:"):
        imageX = argument.split(":")[1].split("x")[0]
        imageY = argument.split(":")[1].split("x")[1]
        try:
            imageSize = (int(imageX), int(imageY))
        except:
            print("invalid image size"); exit()
    elif argument.startswith("start:"):
        imageColor = argument.split(":")[1]
    elif argument.startswith("colors:"):
        pixelColors = argument.split(":")[1].split(",")
    elif argument.startswith("speed:"):
        pixelsPerFrame = int(argument.split(":")[1])
    elif argument.startswith("output:"):
        outputFile = argument.split(":")[1]

locations = []
for x in range(0, imageSize[0], 10):
    for y in range(0, imageSize[1], 10):
        locations.append((x, y))
value = round(len(locations) / pixelsPerFrame) / pixelsPerFrame
if round(value, 3) != value or value <= 0.01:
    print(f"speed ({pixelsPerFrame}) does not match image size {imageSize}"); exit()

frames = []; pixels = {}
imageRGB = tuple(int(imageColor.replace("#", "")[i:i+2], 16) for i in (0, 2, 4))

for index in range(len(pixelColors)):
    pixels[index] = {}; locations = []
    for x in range(0, imageSize[0], 10):
        for y in range(0, imageSize[1], 10):
            locations.append((x, y))

    for i in range(round(len(locations) / pixelsPerFrame)):
        image = Image.new('P', imageSize, imageRGB)
        draw = ImageDraw.Draw(image)

        for layer in pixels:
            for pixel in pixels[layer]:
                draw.rectangle(pixels[layer][pixel], fill = pixelColors[layer])
        
        for i in range(pixelsPerFrame):
            location = random.choice(locations); locations.remove(location)
            shape = [location, (location[0] + 10, location[1] + 10)]
            draw.rectangle(shape, fill = pixelColors[index]); pixels[index][location] = shape
        frames.append(image)

if len(frames) > 0:
    frames[0].save(
        outputFile, save_all=True,
        append_images=frames[1:],
        duration=40, loop=0, optimize=False
    )
else:
    print("image too small")

