from ctypes import Structure



def _struct_proxy_property(name, mutable=True):
    def getter(self):
        return getattr(self._contents, name)

    def setter(self, value):
        setattr(self._contents, name, value)

    return property(getter, setter if mutable else None)

class _StructProxy:
    __slots__ = ('_contents')

    def __new__(cls, /, *args, **kwargs):
        if '_struct_' not in dir(cls):
            raise TypeError('cannot create instance: has no _struct_')

        return super().__new__(cls)

    def __init__(self, struct = None, /):
        if struct is not None:
            self._contents = struct
        else:
            self._contents = self._struct_()

class StructProxyMeta(type):
    def __new__(cls, name, bases, attrs):
        if '_struct_' in attrs:
            hidden = attrs.get('_hidden_fields_', ())

            if not issubclass(attrs['_struct_'], Structure):
                raise TypeError('_struct_ must be a struct')

            for fname, _ in attrs['_struct_']._fields_:
                if fname not in hidden and fname not in attrs:
                    attrs[fname] = _struct_proxy_property(fname, True)

        return super().__new__(cls, name, bases, attrs)

class StructProxy(_StructProxy, metaclass=StructProxyMeta):
    __slots__ = ()

class ImmutableStructProxyMeta(type):
    def __new__(cls, name, bases, attrs):
        if '_struct_' in attrs:
            hidden = attrs.get('_hidden_fields_', ())

            if not issubclass(attrs['_struct_'], Structure):
                raise TypeError('_struct_ must be a struct')

            for fname, _ in attrs['_struct_']._fields_:
                if fname not in hidden and fname not in attrs:
                    attrs[fname] = _struct_proxy_property(fname, False)

        return super().__new__(cls, name, bases, attrs)

class ImmutableStructProxy(_StructProxy, metaclass=ImmutableStructProxyMeta):
    __slots__ = ()
