from django.conf import settings
from PIL import Image, ImageOps, ImageColor, ImageEnhance
from .transform import Transform, Mode

# Adapted from 
# https://stackoverflow.com/a/43738947
def crop_to_aspect(source_image, aspect, divisor=1, alignx=0.5, aligny=0.5):
    """Crops an image to a given aspect ratio.
    Args:
        aspect (float): The desired aspect ratio.
        divisor (float): Optional divisor. Allows passing in (w, h) pair as the first two arguments.
        alignx (float): Horizontal crop alignment from 0 (left) to 1 (right)
        aligny (float): Vertical crop alignment from 0 (left) to 1 (right)
    Returns:
        Image: The cropped Image object.
    """
    if source_image.width / source_image.height > aspect / divisor:
        newwidth = int(source_image.height * (aspect / divisor))
        newheight = source_image.height
    else:
        newwidth = source_image.width
        newheight = int(source_image.width / (aspect / divisor))
    img = source_image.crop((alignx * (source_image.width - newwidth),
                     aligny * (source_image.height - newheight),
                     alignx * (source_image.width - newwidth) + newwidth,
                     aligny * (source_image.height - newheight) + newheight))
    return img

'''
    PIL's exif_transpose sometimes throws an error if exif data contains unexpected values.
    See this issue:
    https://github.com/python-pillow/Pillow/issues/4346
    (if that issue gets fixed, we can probably drop this)
'''
def strip_all_exif_other_than_rotation(image):
    exif = image.getexif()
    # Remove all exif tags
    for k in exif.keys():
        if k != 0x0112:
            exif[k] = None # If I don't set it to None first (or print it) the del fails for some reason. 
        del exif[k]
    # Put the new exif object in the original image
    new_exif = exif.tobytes()
    image.info["exif"] = new_exif

def resize(image:Image, width:int, height:int, mode:Mode, scale_up:bool):
    if mode == Mode.scale:
        if scale_up :
            if (image.width/image.height) > width/height :
                # limit by width, not height
                return image.resize((
                    width,
                    int(image.height/image.width*width)
                ))
            else :
                # limit by height, not by width
                return image.resize((
                    int(image.width/image.height*height),
                    height
                ))
        else :
            image.thumbnail((
                min(width, image.width),
                min(height, image.height)
            ))
            return image

    if mode == Mode.crop:
        # we always crop to aspect ratio
        image = crop_to_aspect(image, width, height)

        # we'll always scale down, but we'll only scale up if explicitly set
        if image.width > width or scale_up :
            image = image.resize((width, height))

        return image

    if mode == Mode.stretch :
        if scale_up :
            return image.resize((width, height))
        else :
            return image.resize((
                min(width, image.width),
                min(height, image.height)
            ))

    raise ValueError(f'Unsupported mode: {mode}')

def handle_crop(image, top, right, bottom, left):
    if not any((top, right, bottom, left)) :
        return image

    # Have to leave at least 1px
    left = min(left, image.width-1)
    top = min(top, image.height-1)

    right = image.width - right
    bottom = image.height - bottom

    # Have to be at least 1px past left/top
    right = max(right, left+1)
    bottom = max(bottom, top+1) 

    return image.crop((left, top, right, bottom))

def handle_overlay(image, overlay):
    if not overlay :
        return image

    color = ImageColor.getcolor(overlay.color, image.mode)

    # Image.alpha_composite only works with RGBA images,
    # but it seems to be the only approach that doesn't what we want with all RGBA images
    if image.mode == 'RGBA' :
        overlay_image = Image.new(image.mode, image.size, color)
        overlay_image.putalpha(int(overlay.alpha * 255))
        return Image.alpha_composite(
            image,
            overlay_image,
        )

    # This approach, when applied to RGBA images, seems to give different results
    # depending on wether background is #0000 or #FFF0 (or any other transparent color)
    return Image.blend(
        image,
        Image.new(image.mode, image.size, color),
        overlay.alpha,
    )

def handle_rotate(image, rotation):
    if not rotation :
        return image

    # store original values
    width, height = image.width, image.height
    # rotate, expanding if needed
    image = image.rotate(rotation, expand=True)
    # crop, as needed
    if rotation in (90, 270):
        image = crop_to_aspect(image, height, width)

    return image

def transform(image: Image, transform: Transform):
    # rotate according to exif data
    try :
        image = ImageOps.exif_transpose(image)
    except Exception :
        strip_all_exif_other_than_rotation(image)
        image = ImageOps.exif_transpose(image)

    # crop fixed amounts from any side
    image = handle_crop(image, transform.crop_top, transform.crop_right, transform.crop_bottom, transform.crop_left)

    width = transform.width
    height = transform.height

    # match_orientation support
    if transform.match_orientation and width and height :
        if (width > height) != (image.width > image.height) :
            width, height = height, width

    # TODO - add focus_left and focus_bottom support
    if width or height :
        image = resize(
            image, 
            width or image.width,
            height or image.height, 
            transform.mode, 
            transform.scale_up,
        )

    for value, enhancer in [
        (transform.color, ImageEnhance.Color),
        (transform.contrast, ImageEnhance.Contrast),
        (transform.brightness, ImageEnhance.Brightness),
    ] :
        if value < 1 :
            image = enhancer(image).enhance(value)

    image = handle_overlay(image, transform.overlay)
    image = handle_rotate(image, transform.rotate)

    # TODO - flipping

    return image
