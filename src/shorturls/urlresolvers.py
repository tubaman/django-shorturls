import urlparse
from django.core.urlresolvers import reverse, NoReverseMatch
from django.conf import settings
from shorturls.baseconv import base62

def get_prefix(obj):
    global _prefixmap
    try:
        _prefixmap
    except NameError:
        _prefixmap = dict((m,p) for p,m in settings.SHORTEN_MODELS.items())
    key = '%s.%s' % (obj._meta.app_label, obj.__class__.__name__.lower())
    return _prefixmap[key]

def get_shorturl(obj):
    try:
        prefix = get_prefix(obj)
    except (AttributeError, KeyError):
        raise NoReverseMatch
    
    tinyid = base62.from_decimal(obj.pk)
    
    if hasattr(settings, 'SHORT_BASE_URL') and settings.SHORT_BASE_URL:
        return urlparse.urljoin(settings.SHORT_BASE_URL, prefix+tinyid)

    return reverse('shorturls.views.redirect', kwargs = {
        'prefix': prefix,
        'tiny': tinyid
    })
