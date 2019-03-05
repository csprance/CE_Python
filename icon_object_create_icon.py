# icon_object_create_icon.py
# Entrada Interactive - Miscreated
# Author: Chris Sprance
# Description: Creates icons automatically
import os
import time
import argparse
import sys

from PIL import Image, ImageOps, ImageFilter, ImageEnhance


def parse_app_args():
    parser = argparse.ArgumentParser(
        description="Create an icon based on some arguments"
    )
    parser.add_argument("--name", help="The name of the item to create an icon for.")
    parser.add_argument(
        "--images",
        nargs="*",
        default=[],
        help="The images from the screenshots folder at the time of the cryengine screenshot.",
    )
    parser.add_argument(
        "--embellishment_48",
        help="The image used to embellish the _48 item with.",
        default=False,
    )
    parser.add_argument(
        "--embellishment_200",
        help="The image used to embellish the _208 item with.",
        default=False,
    )
    parser.add_argument(
        "--embellishment_2048",
        help="The image used to embellish the _2048 item with.",
        default=False,
    )
    parser.add_argument(
        "--embellishment_under",
        help="Should we put the embellishment under or over the image?",
        nargs="*",
        type=int,
        default=False,
    )
    parser.add_argument(
        "--pink",
        default=False,
        help="Remove pink background instead of green.",
        action="store_true",
    )
    icon_type = parser.add_mutually_exclusive_group(required=True)
    icon_type.add_argument(
        "--epic", help="Create an epic purple icon.", default=False, action="store_true"
    )
    icon_type.add_argument(
        "--special",
        help="Create a special orange icon.",
        default=False,
        action="store_true",
    )
    icon_type.add_argument(
        "--standard", help="Create a standard icon.", default=False, action="store_true"
    )
    icon_type.add_argument(
        "--custom_color",
        help="Create an icon with a custom (r,g,b) 0-255 drop shadow.",
        nargs="*",
        type=int,
        default=False,
    )
    return parser.parse_args()


try:
    args = parse_app_args()
except Exception as e:
    print(e)
    os.system("pause")

# #####################################
# Change these options to tweak settings
# #####################################

# the green range to remove (tweak for green things if needed)
GREEN_RANGE_MIN_HSV = (100, 80, 70)
GREEN_RANGE_MAX_HSV = (185, 255, 255)
# sometimes we need to flip to pink for green things
PINK_RANGE_MIN_HSV = (287, 80, 70)
PINK_RANGE_MAX_HSV = (310, 255, 255)
MIN_HSV = PINK_RANGE_MIN_HSV if args.pink else GREEN_RANGE_MIN_HSV
MAX_HSV = PINK_RANGE_MAX_HSV if args.pink else GREEN_RANGE_MAX_HSV

# the final icon size to save
ICON_SIZE = (48, 48)
# needed for steam inventory
ICON_SIZE_LARGE = (200, 200)
ICON_SIZE_XLARGE = (2048, 2048)
# Image.NEAREST, Image.BILINEAR, Image.BICUBIC, or Image.LANCZOS
RESAMPLING_TYPE = Image.ANTIALIAS

# these crop bounds very closely match the icon_guides AreaShape in the IconLevel.cry
CROP_BOUNDS_LEFT = 1085
CROP_BOUNDS_UPPER = 278
CROP_BOUNDS_RIGHT = 2624
CROP_BOUNDS_LOWER = 1817

# shadow options
default_shadow_color = (0, 0, 0)  # black
epic_shadow_color = (147, 107, 202)  # purps
special_shadow_color = (205, 145, 51)  # orange
# r,g,b 0-255 color of the shadow in the icon change to one of above
SHADOW_COLOR = default_shadow_color if args.custom_color is False else args.custom_color
# the opacity of the shadow in the icon 1=opaque 0=transparent
SHADOW_OPACITY = .6
# the blur radius for the gaussian blur (silhouette of the model blurred by this radius)
SHADOW_BLUR_RADIUS = 120


# #####################################
# Constants
# #####################################


def get_all_files(file_type, folder):
    """Get all the files to parse returns an array of paths"""
    file_paths = list()
    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.endswith(file_type):
                file_paths.append(os.path.join(root, f))
    return file_paths


def rgb_to_hsv(r, g, b):
    maxc = max(r, g, b)
    minc = min(r, g, b)
    v = maxc
    if minc == maxc:
        return 0.0, 0.0, v
    s = (maxc - minc) / maxc
    rc = (maxc - r) / (maxc - minc)
    gc = (maxc - g) / (maxc - minc)
    bc = (maxc - b) / (maxc - minc)
    if r == maxc:
        h = bc - gc
    elif g == maxc:
        h = 2.0 + rc - bc
    else:
        h = 4.0 + gc - rc
    h = (h / 6.0) % 1.0
    return h, s, v


def remove_background_chroma(img):
    # Load image and convert it to RGBA, so it contains alpha channel
    im = img.convert("RGBA")
    # Go through all pixels and turn each 'green' pixel to transparent
    pix = im.load()
    width, height = im.size
    for x in range(width):
        for y in range(height):
            r, g, b, a = pix[x, y]
            h_ratio, s_ratio, v_ratio = rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            h, s, v = (h_ratio * 360, s_ratio * 255, v_ratio * 255)
            min_h, min_s, min_v = MIN_HSV
            max_h, max_s, max_v = MAX_HSV
            if min_h <= h <= max_h and min_s <= s <= max_s and min_v <= v <= max_v:
                pix[x, y] = (0, 0, 0, 0)
    return im


def add_drop_shadow(
    image,
    shadow_color=SHADOW_COLOR,
    shadow_opacity=SHADOW_OPACITY,
    blur_radius=SHADOW_BLUR_RADIUS,
):
    # create the shadow blob
    alpha = image.split()[3]
    inverted = ImageOps.invert(alpha)
    blurred = inverted.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    # create the shadow back-plate
    if args.epic:
        shadow_color = epic_shadow_color
    if args.special:
        shadow_color = special_shadow_color
    r, g, b, a = Image.new("RGBA", image.size, color=shadow_color).split()
    enhancer = ImageEnhance.Brightness(ImageOps.invert(blurred))
    shadow_mask = enhancer.enhance(shadow_opacity)
    shadow = Image.merge("RGBA", [r, g, b, shadow_mask])
    # combine the shadow and the original image
    canvas = Image.new("RGBA", image.size, color=(0, 0, 0, 0))
    canvas.paste(shadow)
    canvas.paste(image, mask=image)
    return canvas


def composite_embellishment(image, embellishment):
    # create a blank canvas
    canvas = Image.new("RGBA", image.size, color=(0, 0, 0, 0))
    if args.embellishment_under:
        # paste the embellishment first
        canvas.paste(embellishment, mask=embellishment)
        # paste in the original image second
        canvas.paste(image, mask=image)
    else:
        # paste the image
        canvas.paste(image, mask=image)
        # paste in the embellishment second
        canvas.paste(embellishment, mask=embellishment)
    # return the new composite image
    return canvas


def log_it(line):
    print(line)
    filename = os.path.abspath(
        os.path.join(os.path.dirname(sys.executable), "..", "icon_object_log.txt")
    )
    write_mode = "a" if os.path.exists(filename) else "w"
    with open(filename, write_mode) as log_file:
        log_file.write(line + "\n")


def create_icon():
    # get the screenshot dir
    if getattr(sys, "frozen", False):
        screenshot_dir = os.path.abspath(
            os.path.join(
                os.path.dirname(sys.executable), "..", "..", "..", "user", "screenshots"
            )
        )
        icon_folder = os.path.abspath(
            os.path.join(
                os.path.dirname(sys.executable),
                "..",
                "..",
                "..",
                "GameSDK",
                "Libs",
                "UI",
                "Inventory",
                "item_images",
            )
        )
        icon_folder_large = os.path.abspath(
            os.path.join(
                os.path.dirname(sys.executable), "..", "..", "..", "EI", "icons"
            )
        )
    else:
        screenshot_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "user", "screenshots")
        )
        icon_folder = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "GameSDK",
                "Libs",
                "UI",
                "Inventory",
                "item_images",
            )
        )
        icon_folder_large = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "EI", "icons")
        )
    # move into to the screenshot directory
    os.chdir(screenshot_dir)
    # get the screenshot name
    name = args.name
    # get the files
    files_from_crytek = set(args.images)
    # wait to make sure it saves the screenshot
    time.sleep(1)
    # check the screenshots folder again to get the new files list
    files_after_screenshot = set(get_all_files(".jpg", screenshot_dir))
    # compare the files lists together to get the newest screenshot
    screenshot = list(files_after_screenshot - files_from_crytek)[0]
    # Load the screenshot
    img = Image.open(screenshot)
    # crop it
    cropped_image = crop_image(img)
    # remove the chroma background
    transparent_image = remove_background_chroma(cropped_image)
    # add the drop shadow
    drop_shadowed_image = add_drop_shadow(transparent_image)

    # #############
    # resize it to 2048
    # #############
    xlarge_transparent_image = transparent_image.resize(
        ICON_SIZE_XLARGE, resample=RESAMPLING_TYPE
    )
    # add embellishment if needed
    if args.embellishment_2048:
        xlarge_transparent_image = composite_embellishment(
            xlarge_transparent_image, Image.open(args.embellishment_2048)
        )
    # move into the icon folder large
    os.chdir(icon_folder_large)
    # save the xlarge image
    icon_name_xlarge = "%s_%s.png" % (name, ICON_SIZE_XLARGE[0])
    xlarge_transparent_image.save(icon_name_xlarge)

    # #############
    # resize it to 200
    # #############
    large_transparent_image = transparent_image.resize(
        ICON_SIZE_LARGE, resample=RESAMPLING_TYPE
    )
    # add embellishment if needed
    if args.embellishment_200:
        large_transparent_image = composite_embellishment(
            large_transparent_image, Image.open(args.embellishment_200)
        )
    # save it with the correct name
    icon_name_large = "%s_%s.png" % (name, ICON_SIZE_LARGE[0])
    large_transparent_image.save(icon_name_large)

    # #############
    # resize it to 48
    # #############
    small_transparent_image = drop_shadowed_image.resize(
        ICON_SIZE, resample=RESAMPLING_TYPE
    )
    # add embellishment if needed
    if args.embellishment_48:
        small_transparent_image = composite_embellishment(
            small_transparent_image, Image.open(args.embellishment_48)
        )
    # move into the icon folder small
    os.chdir(icon_folder)
    # save it with the correct name
    icon_name = "%s_%s.png" % (name, ICON_SIZE[0])
    small_transparent_image.save(icon_name)

    # log it
    log_it(icon_folder_large + "\\" + icon_name_large)
    log_it(icon_folder_large + "\\" + icon_name_xlarge)
    log_it(icon_folder + "\\" + icon_name)


def crop_image(img):
    return img.crop(
        (CROP_BOUNDS_LEFT, CROP_BOUNDS_UPPER, CROP_BOUNDS_RIGHT, CROP_BOUNDS_LOWER)
    )


if __name__ == "__main__":
    try:
        create_icon()
    except Exception as e:
        print(e)
        try:
            create_icon()
        except Exception as e:
            print(e)
            os.system("pause")
