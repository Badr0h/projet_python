from django.conf import settings

def media_url(request):
    """Adds MEDIA_URL to the template context."""
    return {'MEDIA_URL': settings.MEDIA_URL}
