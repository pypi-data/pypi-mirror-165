from django import http
from django.conf import settings
from django.contrib.staticfiles import finders
from django.views.generic import View
from io import BytesIO
import mimetypes
from pathlib import Path
from PIL import Image, UnidentifiedImageError

from ._etag_responder import ETagResponder
from .transform import Transform, TransformParseError
from ._operations import transform
from . import validator

def iter_possible_local_file_locations(source_url):
    if not source_url.startswith('/') :
        return

    static_url = getattr(settings, 'STATIC_URL')
    if static_url and source_url.startswith(static_url):
        path = source_url[len(static_url):]

        # Is it the path to a "collectstatic-ed" file? (ie. live server)
        static_root = getattr(settings, 'STATIC_ROOT')
        if static_root :
            yield Path(static_root, *path.split('/'))

        # Is it an uncollected static file? (ie. dev server)
        path = finders.find(path)
        if path :
            yield Path(path)

    # Is it the path to a local media file?
    media_url = getattr(settings, 'MEDIA_URL')
    media_root = getattr(settings, 'MEDIA_ROOT')
    if media_url and media_root and source_url.startswith(media_url):
        path = source_url[len(media_url):]
        yield Path(media_root, *path.split('/'))

def get_file_path(source):
    for path in iter_possible_local_file_locations(source):
        if path.is_file() :
            return path
    raise http.Http404()

class ImageResponder(ETagResponder):
    def __init__(self, request, transform, source):
        validator._validator.validate_request(request, transform, source)

        # may raise 404
        self.source_path = get_file_path(source)

        self.etag = f'"{self.source_path.stat().st_mtime}"'

        # may raise TransformParseError
        self.transform = Transform.from_string(transform)

        validator._validator.validate_parsed_transform(request, self.transform)
        validator._validator.validate_local_source_file(request, str(self.source_path))

    def build_response(self):
        # may raise UnidentifiedImageError
        image = Image.open(self.source_path)

        # Save this, because various PIL operations return a new image with no format set
        image_format = image.format

        try :
            image = transform(image, self.transform)
            content_buffer = BytesIO()
            image.save(content_buffer, image_format)
        finally :
            image.close()

        content_buffer.seek(0)

        return http.HttpResponse(
            content_buffer.read(),
            content_type=Image.MIME[image_format],
        )

    @classmethod
    def handle(cls, request, transform):
        path_query = request.get_full_path().split('?', 1)
        try :
            source = path_query[1]
        except IndexError :
            source = ''

        try :
            return super().handle(request, transform, source)
        except TransformParseError as e :
            return http.HttpResponseBadRequest(str(e))
        except validator.ValidationError as e :
            return http.HttpResponseForbidden(str(e))
        except UnidentifiedImageError as e :
            return http.HttpResponseBadRequest(b'File could not be interpereted as an image')
