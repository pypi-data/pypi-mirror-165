# 2.0.0
Changed url format (put source in querystring, rather than path), 
to avoid issue with apache removing empty segments from url paths.

Backward compatible with 1.x iff you always use our utils for url generation 
(you'll need to adjust if you manually generate urls).

### 1.0.1
Explicit Django 2.2 support

# 1.0.0