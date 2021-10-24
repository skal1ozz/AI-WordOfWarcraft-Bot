from .abstract_backend import AbstractBackend


def wrapper_backend_required(fn):
    def wr(self, *args, **kwargs):
        backend = getattr(self, 'backend', None)
        if not isinstance(backend, AbstractBackend):
            raise AttributeError('Backend should be a child of '
                                 'AbstractKeyboardBackend')
        return fn(self, *args, **kwargs)
    return wr
