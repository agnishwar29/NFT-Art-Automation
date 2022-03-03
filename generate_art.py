from PIL import Image, ImageDraw, ImageChops
import random
import colorsys

from PIL.Image import ANTIALIAS


def random_color():
    h = random.random()
    s = 1
    v =1
    float_rgb = colorsys.hsv_to_rgb(h,s,v)
    rgb = [int(i*255) for i in float_rgb]

    return tuple(rgb)

def interpolate(start_color,end_color, factor:float):
    recip = 1 - factor
    return (
        int(start_color[0] * recip + end_color[0] * factor),
       int(start_color[1] * recip + end_color[1] * factor),
        int(start_color[2] * recip + end_color[2] * factor),
    )


def generate_art(path: str):
    print("Generating Art")
    target_size = 600
    scale_factor = 2
    image_size_px = target_size * scale_factor
    padding_px = 16 * scale_factor
    image_bg_color = (0,0,0)
    start_color = random_color()
    end_color= random_color()
    image = Image.new("RGB", size=(image_size_px,image_size_px),color=image_bg_color)

    draw = ImageDraw.Draw(image)

    points = []

    #generate the points
    for _ in range(10):
        random_point = (random.randint(padding_px,image_size_px-padding_px),
                        random.randint(padding_px,image_size_px-padding_px))
        points.append(random_point)

    min_x = min([i[0] for i in points])
    max_x = max([i[0] for i in points])

    min_y = min([i[1] for i in points])
    max_y = max([i[1] for i in points])

    #Centering the image
    delta_x = min_x - (image_size_px - max_x)
    delta_y = min_y - (image_size_px - max_y)

    for i, point in enumerate(points):
        points[i] = (point[0] - delta_x //2, point[1]- delta_y//2)

    # Drawing the points
    thickness = 0
    n_points = len(points) -1
    for i, point in enumerate(points):
        #overlay canvas
        overlay_image = Image.new("RGB", size=(image_size_px, image_size_px), color=image_bg_color)
        overlay_draw = ImageDraw.Draw(overlay_image)

        p1 = point
        if i == n_points:
            p2 = points[0]
        else:
            p2 = points[i+1]
        line_xy= ((p1, p2))
        color_factor = i/n_points
        line_color = interpolate(start_color, end_color,color_factor)
        thickness +=1 * scale_factor
        overlay_draw.line(line_xy, fill=line_color, width=thickness)
        image = ImageChops.add(image, overlay_image)

    image = image.resize((target_size, target_size), resample=ANTIALIAS)
    image.save(path)

if __name__ == '__main__':
    for i in range(10):
        generate_art(f"{i}.png")