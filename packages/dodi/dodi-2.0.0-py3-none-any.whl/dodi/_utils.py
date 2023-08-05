from django import urls
from django.conf import settings
from django.templatetags.static import static
from urllib.parse import urlencode

def get_base():
    return getattr(settings, 'DODI_BASE_URL', '/')

def url(source:str, transform:str):
    '''
    Return a url for the given source and transformation options, 
    in "canonical form" (helps with cache efficiency).

    Will throw a resolver error if dodi isn't installed.

    Will usually return a site-relative url. If you serve your site from 
    multiple domains, you may want to set an absolute value for 
    DODI_BASE_URL, in which case this will return an absolute url.
    '''
    return (
        get_base().rstrip('/')
        + urls.reverse('dodi_image', kwargs=dict(transform=transform))
        + '?' + source
    )
def static_url(static_path:str, transform:str):
    '''
    Calls static() on the given path, rather than naively prepending STATIC_URL.
    This ensures that any cache-busting components in the url remain
    (ie. if using ManifestStaticFilesStorage)
    '''
    return url(static(static_path), transform)

def url_base():
    '''
    Useful if you want to pass this to js so you can construct urls on the client side.
    '''
    return url('x', 'x')[:-3]