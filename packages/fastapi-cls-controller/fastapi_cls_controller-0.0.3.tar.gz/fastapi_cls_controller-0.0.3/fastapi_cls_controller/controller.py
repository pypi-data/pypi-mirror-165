import inspect
from typing import Callable, List, Type, TypeVar

from fastapi import APIRouter, Depends
from starlette.routing import Route, WebSocketRoute

__PATH_PREFIX = "/__@@__"
__router = APIRouter(prefix=__PATH_PREFIX)
get = __router.get
post = __router.post
put = __router.put
patch = __router.patch
delete = __router.delete
head = __router.head
options = __router.options
websocket_route = __router.websocket_route
T = TypeVar("T")


def controller(*args, **kwargs) -> Callable[[Type[T]], Type[T]]:
    def decorator(c_class: Type[T]) -> Type[T]:
        orig_init = c_class.__init__

        def __init__(self, *args_, **kwargs_):
            orig_init(self, *args_, **kwargs_)
            c_router = APIRouter(*args, **kwargs)
            function_members = inspect.getmembers(self.__class__, inspect.isfunction)
            functions_set = set(func for _, func in function_members)
            c_class_routes = [
                route
                for route in __router.routes
                if isinstance(route, (Route, WebSocketRoute))
                and route.endpoint in functions_set
            ]
            for c_route in c_class_routes:
                c_route.path = c_router.prefix + c_route.path.split(__PATH_PREFIX)[1]
                c_route.tags = c_router.tags  # type: ignore
                __router.routes.remove(c_route)
                _update_route_signature(self, c_route)
                c_router.routes.append(c_route)

            self.router = c_router
            self.routes = c_router.routes
            self.default_response_class = c_router.default_response_class
            self.generate_unique_id_function = c_router.generate_unique_id_function
            self.on_startup = c_router.on_startup
            self.on_shutdown = c_router.on_shutdown

        c_class.__init__ = __init__
        return c_class

    return decorator


def _update_route_signature(c_instance, route) -> None:
    def identity():
        return c_instance

    old_endpoint = route.endpoint
    old_signature = inspect.signature(old_endpoint)
    old_parameters: List[inspect.Parameter] = list(old_signature.parameters.values())
    old_first_parameter = old_parameters[0]
    new_first_parameter = old_first_parameter.replace(default=Depends(identity))
    new_parameters = [new_first_parameter] + [
        parameter.replace(kind=inspect.Parameter.KEYWORD_ONLY)
        for parameter in old_parameters[1:]
    ]
    new_signature = old_signature.replace(parameters=new_parameters)
    setattr(route.endpoint, "__signature__", new_signature)
