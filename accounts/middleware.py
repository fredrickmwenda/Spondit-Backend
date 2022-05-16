from datetime import datetime
from logging import getLogger
from django.urls.exceptions import Resolver404


logger = getLogger(__file__)


class HandleRouteNotFoundMiddleware:

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        try:
            inner_instance = self.inner(scope)
            return inner_instance
        except (Resolver404, ValueError) as e:
            if 'No route found for path' not in str(e) and \
               scope["type"] not in ['http', 'websocket']:
                raise e

            logger.warning(
                f'{datetime.now()} - {e} - {scope}'
            )

            if scope["type"] == "http":
                return self.handle_http_route_error
            elif scope["type"] == "websocket":
                return self.handle_ws_route_error

    async def handle_ws_route_error(self, receive, send):
        await send({"type": "websocket.close"})

    async def handle_http_route_error(self, receive, send):
        await send({
            "type": "http.response.start",
                    "status": 404,
                    "headers": {},
        })
        await send({
            "type": "http.response.body",
            "body": "",
            "more_body": "",
        })