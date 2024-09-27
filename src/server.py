import falcon
from src.api.resource import MailResource


class HelloWorldResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # HTTP status code
        resp.media = {"message": "Hello, World!"}


# Create Falcon API instance
app = falcon.App(middleware=[falcon.CORSMiddleware(allow_origins="*", allow_credentials="*")])

# Add route to HelloWorldResource
hello_world = HelloWorldResource()
app.add_route("/hello", hello_world)
app.add_route("/email/action", MailResource())
