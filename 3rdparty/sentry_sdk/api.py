import inspect
from contextlib import contextmanager

from sentry_sdk.hub import Hub
from sentry_sdk.scope import Scope


MYPY = False
if MYPY:
    from typing import Any
    from typing import Optional
    from typing import overload
    from typing import Callable
    from typing import TypeVar
    from contextlib import ContextManager

    from sentry_sdk.utils import Event, Hint, Breadcrumb, BreadcrumbHint

    T = TypeVar("T")
    F = TypeVar("F", bound=Callable[..., Any])
else:

    def overload(x):
        # type: (T) -> T
        return x


__all__ = [
    "capture_event",
    "capture_message",
    "capture_exception",
    "add_breadcrumb",
    "configure_scope",
    "push_scope",
    "flush",
    "last_event_id",
]


def hubmethod(f):
    # type: (F) -> F
    f.__doc__ = "%s\n\n%s" % (
        "Alias for `Hub.%s`" % f.__name__,
        inspect.getdoc(getattr(Hub, f.__name__)),
    )
    return f


@hubmethod
def capture_event(event, hint=None):
    # type: (Event, Optional[Hint]) -> Optional[str]
    hub = Hub.current
    if hub is not None:
        return hub.capture_event(event, hint)
    return None


@hubmethod
def capture_message(message, level=None):
    # type: (str, Optional[str]) -> Optional[str]
    hub = Hub.current
    if hub is not None:
        return hub.capture_message(message, level)
    return None


@hubmethod
def capture_exception(error=None):
    # type: (Optional[BaseException]) -> Optional[str]
    hub = Hub.current
    if hub is not None:
        return hub.capture_exception(error)
    return None


@hubmethod
def add_breadcrumb(crumb=None, hint=None, **kwargs):
    # type: (Optional[Breadcrumb], Optional[BreadcrumbHint], **Any) -> None
    hub = Hub.current
    if hub is not None:
        return hub.add_breadcrumb(crumb, hint, **kwargs)


@overload  # noqa
def configure_scope():
    # type: () -> ContextManager[Scope]
    pass


@overload  # noqa
def configure_scope(callback):
    # type: (Callable[[Scope], None]) -> None
    pass


@hubmethod  # noqa
def configure_scope(
    callback=None  # type: Optional[Callable[[Scope], None]]
):
    # type: (...) -> Optional[ContextManager[Scope]]
    hub = Hub.current
    if hub is not None:
        return hub.configure_scope(callback)
    elif callback is None:

        @contextmanager
        def inner():
            yield Scope()

        return inner()
    else:
        # returned if user provided callback
        return None


@overload  # noqa
def push_scope():
    # type: () -> ContextManager[Scope]
    pass


@overload  # noqa
def push_scope(callback):
    # type: (Callable[[Scope], None]) -> None
    pass


@hubmethod  # noqa
def push_scope(
    callback=None  # type: Optional[Callable[[Scope], None]]
):
    # type: (...) -> Optional[ContextManager[Scope]]
    hub = Hub.current
    if hub is not None:
        return hub.push_scope(callback)
    elif callback is None:

        @contextmanager
        def inner():
            yield Scope()

        return inner()
    else:
        # returned if user provided callback
        return None


@hubmethod
def flush(timeout=None, callback=None):
    # type: (Optional[float], Optional[Callable[[int, float], None]]) -> None
    hub = Hub.current
    if hub is not None:
        return hub.flush(timeout=timeout, callback=callback)


@hubmethod
def last_event_id():
    # type: () -> Optional[str]
    hub = Hub.current
    if hub is not None:
        return hub.last_event_id()
    return None