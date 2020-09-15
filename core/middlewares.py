from datetime import date

from django.utils import timezone


class TrackActionsMiddleware(object):
    """
    Simple middleware to track last login and last action.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            if request.user.last_login != date.today():
                request.user.last_login = date.today()
                request.user.last_action = timezone.now()
                request.user.save(update_fields=["last_login", "last_action"])
            else:
                request.user.last_action = timezone.now()
                request.user.save(
                    update_fields=[
                        "last_action",
                    ]
                )

        return response
