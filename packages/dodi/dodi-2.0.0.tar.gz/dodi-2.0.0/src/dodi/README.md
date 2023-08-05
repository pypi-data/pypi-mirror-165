# DODI: Django On-Demand Images

Creates modified images at request time, _not_ page request / template rendering time. 
Works with both static files and media files.

## Installation:

`pip install dodi`

urls.py:
```py
urlpatterns = [
    ...,
    path('dodi/', include('dodi.urls')),
    ...,
]
```

## Usage

Just request images via urls with the format /dodi/TRANSFORM?SOURCE.

SOURCE is the site-relative url of a self-hosted static file or media file.

TRANSFORM is a semicolon-separate list of options (key=value pairs) and flags. Available transforms/flags are described below.

IE: `/dodi/width=400;height=300;match_orientation?/static/my_app/logo.png`

While you _could_ construct these urls manually, we provide a few utility functions that you should use instead: `dodi.url()`, `dodi.static_url()`, and `dodi.url_base()`. See src/dodi/\_utils.py for details.

### In Django Templates
We haven't added template tags yet, because we use html_generators rather than django templates. Might add later.

## Explicit Cropping

You can specify any of crop_left, crop_right, crop_top, crop_bottom. Pass an integer, representing the number of pixels to crop from that edge.

`crop_left=50;crop_top=100`: crop 50px from the left edge, and 100px from the top.

This happens _before_ any resizing.

## Resizing

To resize, you must specify width and/or height (as integers). There are 3 "modes" of resizing

### mode=scale (default)
`width=300;height=200` / `width=300;height=200;mode=scale`
Scale the image to fit within 300x200 pixels. If the aspect ratio doesn't match, one dimension will be smaller than.

### mode=crop
`width=300;height=200;mode=crop`
Center-crop the image to a 3x2 aspect ratio, then scale to size.

### mode=stretch
`width=300;height=200;mode=stretch`
Stretch/distort the image so that it's 300x200, without cropping.

## Resize Flags

There are some flags that affect resizing. They affect all modes the same way.

### scale_up
`width=1600;height=900;scale_up`
By default, we'll never _increase_ either of an image's dimensions. If this flag is set, we will.

### match_orientation
`width=300;height=200;mode=crop;match_orientation`
If the image is landscape (width>height), then return a 300x200 image. If it's portrait, return a 200x300 image. Useful when you have a collection of landscape/portrait images, and you want them all to have the same area.

## Other Manipulations

### overlay
Add a semi-transparent colored overlay over top of the image.

Takes a "color,alpha" pair, where 0 <= alpha <= 1, and color is any CSS color that can be understood by PIL.

Ie. `overlay=green,0.5` or `overlay=#000,0.8`

## color / contrast / brightness
All take values from 0 to 1. All default to 1.

`color=0`: black and white, `color=1`: original image
`contrast=0`: solid gray, `contrast=1`: original image
`brightness=0`: solid black, `brightness=1`: original image

### rotate
Allowed values are 0, 90, 180, 270.
`rotate=90`: rotate 90 degrees counter-clockwise

## Caching / Immutable Sources

We don't cache images at all. Instead, we send far-future expiry headers. We send an ETag header and handle conditional requests properly.

Web browsers will cache our images. You can configure your web server to cache them, too, so we never have to generate the same image twice.

This all relies on your source urls being "immutable". That is, we expect the image at a given static or media url to never change. This will work automatically for static files if you use ManifestStaticFilesStorage (django's default when DEBUG=False). For media files, it means you should be careful to set the `upload_to` option such that the upload path/name is guaranteed to change every time the field is changed (a new image is uploaded).

### Multiple Domains / DODI_BASE_URL
If you're running your site under multiple domains (ie. en.foo.com and fr.foo.com), they are likely serving the same static/media files. If you have your web server set up to cache responses, it likely uses the absolute url as the cache key. 

Even though en.foo.com/dodi/TRANSFORM/SOURCE and fr.foo.com/dodi/TRANSFORM/SOURCE refer to the same image, they will be generated and cached separately.

In this case, (in your settings.py) you should set `DODI_BASE_URL` to an absolute url (ie. `https://en.foo.com`). With this setup, all of our url-generating utilities will generate absolute urls, so that images are always requested from the same domain.

## Authorization

TODO - document how to use dodi.validator if user wants to add stricter validation/authorization.

## Tests

We have two types of tests setup.

`python -m tests.test_basic` runs through an automated set of tests. `tox` will run these in all of our test environments.

We also have visual tests, requiring you to verify correctness. `python manage.py runserver 8000`, then go open localhost:8000 in your web browser, and verify that the transformed images are as expected.

## TODO

Support for "focal point" (focal_point_left and focal_point_bottom) -> affects how mode=crop behaves.

SVG to PNG support

validator documentation and tests
