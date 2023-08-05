from enum import Enum
import re
from PIL import ImageColor
from typing import Optional

class TransformParseError(Exception):
    pass

class Mode(Enum):
    '''
    How image resizing should be handled.
    '''
    scale = 'scale'
    crop = 'crop'
    stretch = 'stretch'

class OverlayColor:
    def __init__(self, string):
        try :
            c, a = string.split(',')
        except ValueError :
            raise ValueError('OverlayColor must be specified as "color,alpha"')

        # Make sure it's parseable by PIL, but don't save the value
        # PIL will throw value error if color is invalid
        ImageColor.getrgb(c)

        self.color = c
        try :
            self.alpha = float(a)
        except ValueError:
            raise ValueError(f'Invalid OverlayColor alpha part: {a}')

        if not 0 <= self.alpha <= 1 :
            raise ValueError(f'OverlayColor alpha part ({a}) must be between 0 and 1.')            
class Rotation(int):
    def __new__(cls, value):
        message = f'Invalid rotation: {value}. The only allowed rotations are 0, 90, 180, and 270'
        try :
            value = int.__new__(cls, value)
        except ValueError :
            raise ValueError(message)
        if value not in [0,90,180,270] :
            raise ValueError(message)
        return value

class Transform:
    '''
    A description of an image transformation.
    '''
    def __init__(
        self, *,
        crop_left:int=0,
        crop_right:int=0,
        crop_top:int=0,
        crop_bottom:int=0,
        width:int=0,
        height:int=0,
        mode:Mode=Mode.scale,
        overlay:Optional[OverlayColor]=None,
        rotate:Rotation=Rotation(0),
        color:float=1,
        contrast:float=1,
        brightness:float=1,
        scale_up:bool=False,
        match_orientation:bool=False,
    ) :
        self.crop_left = crop_left
        self.crop_right = crop_right
        self.crop_top = crop_top
        self.crop_bottom = crop_bottom
        self.width = width
        self.height = height
        self.mode = mode
        self.overlay = overlay
        self.rotate = rotate
        self.color = color
        self.contrast = contrast
        self.brightness = brightness
        self.scale_up = scale_up
        self.match_orientation = match_orientation

    @classmethod
    def from_string(cls, transform:str):
        '''
        Parse the string and return a valid Transform.
        Raise TransformParseError if in any invalid options are specified.
        '''
        parts = transform.split(';')
        flags = [part for part in parts if '=' not in part]
        options = dict(
            part.split('=', 1)
            for part in parts if '=' in part
        )

        unsupported = set(flags)-set([
            'scale_up',
            'match_orientation',
        ])
        if unsupported :
            raise TransformParseError(f'Unsupported flags: {", ".join(unsupported)}')

        kwargs = {flag: True for flag in flags}

        for option in [
            'color', 'contrast', 'brightness',
        ] :
            value = options.pop(option, None)
            if value is None :
                continue
            try :
                value = float(value)
                if not 0 <= value <= 1 :
                    raise ValueError()
            except ValueError :
                raise TransformParseError(f'Invalid {option}: "{value}". Must be a float between 0 and 1')
            kwargs[option] = value

        for option in [
            'width', 'height',
            'crop_left', 'crop_right', 'crop_top', 'crop_bottom',
        ]:
            value = options.pop(option, None)
            if value is not None :
                try :
                    value = int(value)
                except ValueError :
                    raise TransformParseError(f'Invalid value for {option}: "{value}". Must be an integer')
                if value < 0 :
                    raise TransformParseError(f'{option} must be >= 0')
                kwargs[option] = value

        mode = options.pop('mode', None)
        if mode is not None :
            try :
                kwargs['mode'] = Mode(mode)
            except ValueError :
                raise TransformParseError(f'invalid mode: {mode}')

        overlay = options.pop('overlay', None)
        if overlay :
            try :
                kwargs['overlay'] = OverlayColor(overlay)
            except ValueError as e:
                raise TransformParseError(str(e))

        rotate = options.pop('rotate', None)
        if rotate :
            try :
                kwargs['rotate'] = Rotation(rotate)
            except ValueError as e:
                raise TransformParseError(str(e))

        if options :
            raise TransformParseError(
                f'Unsupported options: {", ".join(options.keys())}'
            )

        return cls(**kwargs)