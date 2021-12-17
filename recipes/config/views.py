from django.http import HttpResponse


def index(request):
    """
    Index view used for health check
    """
    return HttpResponse("200 OK", content_type="text/plain")
