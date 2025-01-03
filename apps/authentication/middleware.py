from django.core.exceptions import PermissionDenied

class BlockLocalUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') and request.user.is_authenticated and (request.user.user_type != 'global' or not request.user.is_staff):
            raise PermissionDenied
        response = self.get_response(request)
        return response