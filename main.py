#!/usr/bin/python3

import random
import sys

from PIL import Image, ImageDraw

pixels_per_frame = 8
output_file = "output.gif"
image_size = (400, 200)
image_color = "#000000"
pixel_colors = ["#ff0000", "#00ff00", "#0000ff", "#000000"]

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
pixelgenerator size:400x200 start:#0068db speed:16 colors:#ff0000,#00ff00 output:file.gif""")
        exit()
    elif argument.startswith("size:"):
        image_x = argument.split(":")[1].split("x")[0]
        image_y = argument.split(":")[1].split("x")[1]
        try:
            image_size = (int(image_x), int(image_y))
        except:
            print("invalid image size")
            exit()
    elif argument.startswith("start:"):
        image_color = argument.split(":")[1]
    elif argument.startswith("colors:"):
        pixel_colors = argument.split(":")[1].split(",")
    elif argument.startswith("speed:"):
        pixels_per_frame = int(argument.split(":")[1])
    elif argument.startswith("output:"):
        output_file = argument.split(":")[1]

locations = []
for x in range(0, image_size[0], 10):
    for y in range(0, image_size[1], 10):
        locations.append((x, y))
value = round(len(locations) / pixels_per_frame) / pixels_per_frame
if round(value, 3) != value or value <= 0.01:
    print(f"speed ({pixels_per_frame}) does not match image size {image_size}")
    exit()

frames = []
image_rgb = tuple(int(image_color.replace("#", "")[i : i + 2], 16) for i in (0, 2, 4))

for index in range(len(pixel_colors)):
    image = Image.new("P", image_size, image_rgb)
    draw = ImageDraw.Draw(image)
    draw.rectangle(
        [(0, 0), image_size],
        fill=image_color if index <= 0 else pixel_colors[index - 1],
    )

    locations = []
    for x in range(0, image_size[0], 10):
        for y in range(0, image_size[1], 10):
            locations.append((x, y))

    frames.append(image.copy())

    for i in range(round(len(locations) / pixels_per_frame)):
        for i in range(pixels_per_frame):
            location = random.choice(locations)
            locations.remove(location)

            shape = [location, (location[0] + 10, location[1] + 10)]
            draw.rectangle(shape, fill=pixel_colors[index])

        frames.append(image.copy())

if len(frames) > 0:
    frames[0].save(
        output_file,
        save_all=True,
        append_images=frames[1:],
        duration=40,
        loop=0,
        optimize=False,
    )
else:
    print("image too small")
