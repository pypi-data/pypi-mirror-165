from django.http import HttpRequest
import os
from typing import Type

from dodi.transform import Transform

class ValidationError(Exception):
    '''
    An exception raised when a transform string fails to parse,
    contains illegal operations, or the request is not authorized.
    '''
    pass

class Validator:
    '''
    A class for validating various steps in dodi's view.

    Each validation function should either do nothing, or raise
    a ValidationError, with a meaningful message.

    Our default validator is intentionally permissive.
    Users can override to more restrictive, if required.
    '''
    @classmethod
    def validate_request(cls, request:HttpRequest, transform:str, source:str):
        '''
        Runs on every request, whether or not transform represents a valid 
        Transform or source represents a valid source image
        '''
        pass

    @classmethod
    def validate_parsed_transform(cls, request:HttpRequest, transform:Transform):
        # We only validate dimensions when scale_up is True 
        # (otherwise they are limited by source image)
        # This is here mainly to protect against user error
        # (ie. js widget lets user dynamically resize image, 
        # and user accidentally enters too many 0's)
        if transform.scale_up :
            if transform.width > 2000 or transform.height > 2000 :
                raise ValueError('When scaling up, maximum dimensions are 2000x2000')

    @classmethod
    def validate_local_source_file(cls, request:HttpRequest, absolute_path:str):
        pass

_validator = Validator
def set_validator(validator_class: Type[Validator]):
    '''
    Specifies which Validator dodi should use when validating requests.

    If users are overriding our Validator, they should call this at
    server start (ie. in urls.py)
    '''
    _validator = validator_class
