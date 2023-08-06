from .models import user_seen


class LastActiveMiddleware(object):
    """
    Middlewate to set timestampe when a user
    has been last seen
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:
            if hasattr(request.user, 'is_impersonate') == False or getattr(request.user, 'is_impersonate') == False:
                user_seen(request.user)

        return self.get_response(request)
