from django import http

class ETagResponder:
    '''
    Helper class for writing a view function supporting etags 
    and conditional requests.

    Users should subclass, implementing build_response and __init__.

    The .handle() classmethod is the final view function.
    '''
    max_age = 31536000 # 1 year - widely recommended maximum value

    def __init__(self, request, *view_args, **view_kwargs):
        '''
        Subclasses must implement __init__
        It must compute etag and store on self.etag
        It must store any other data needed by build_response
        Try to keep this as light as possible - it will be called even for
        conditional requests.
        '''
        raise NotImplementedError()
    def build_response(self) -> http.HttpResponse:
        '''
        Subclasses must implement.
        Will _not_ be called for conditional requests if client had fresh copy.
        Do the heavy lifting here.
        You don't need to set caching headers. We'll do that afterwards.
        '''
        raise NotImplementedError()
    @classmethod
    def handle(cls, request, *args, **kwargs):
        '''
        Subclasses _may_ override (calling super())
        (ie. to provide exception handling or authorization)
        '''
        return cls(request, *args, **kwargs)._get_response(request)

    def _with_cache_headers(self, response):
        max_age = self.max_age
        if not max_age :
            return response

        response['ETag'] = self.etag
        response['Cache-Control'] = f'public, max-age={max_age}'
        return response
        
    def _get_response(self, request):
        # TODO - validate etag?

        # reminder - If-None-Match header may contain multiple comma-separate e-tags.
        # Each e-tag should be quoted, so simple substring match should be sufficient
        if self.etag and self.etag in request.headers.get('if-none-match', ''):
            return self._with_cache_headers(http.HttpResponseNotModified())
        return self._with_cache_headers(self.build_response())
