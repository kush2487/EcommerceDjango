

class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("Before the view is called")

        # Process the request before the view
        response = self.get_response(request)

        print("After the view is called")
        # Process the response
        return response
