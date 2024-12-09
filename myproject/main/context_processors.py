from .models import DisplaySettings

def display_settings(request):
    try:
        settings = DisplaySettings.objects.first()
        return {
            "show_header": settings.show_header if settings else True,
            "show_footer": settings.show_footer if settings else True,
        }
    except DisplaySettings.DoesNotExist:
        return {
            "show_header": True,
            "show_footer": True,
        }
