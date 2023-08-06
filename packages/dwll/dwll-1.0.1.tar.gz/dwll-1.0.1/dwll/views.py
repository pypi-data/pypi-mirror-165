
from django.http import HttpResponseRedirect

from . import signals

from .languages import languages

def change_language(request, name):
    resp, lang = languages.change_language(request, name)
            
    if resp:
        signals.language_changed.send(sender='change_language', user=request.user, language=lang)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
