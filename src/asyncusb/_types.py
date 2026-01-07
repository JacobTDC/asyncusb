import asyncio
import collections.abc
from ctypes import Structure
from functools import wraps
from inspect import signature
from types import GenericAlias
from weakref import WeakKeyDictionary, ref



def _struct_proxy_property(name, mutable=True):
    def getter(self):
        return getattr(self._contents, name)

    if mutable:
        def setter(self, value):
            setattr(self._contents, name, value)
    else:
        setter = None

    return property(getter, setter)

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



#class ScopedSingletonMeta(type):
#    def __init__(self, name, bases, attrs):
#        self.__instance_dict = WeakKeyDictionary()
#
#        # Restore the signature.
#        sig = signature(self.__init__)
#        parameters = tuple(sig.parameters.values())
#        self.__signature__ = sig.replace(parameters=parameters[1:])
#
#        return super().__init__(name, bases, attrs)
#
#    def __call__(self, scope, /, *args, **kwargs):
#        if scope in self.__instance_dict:
#            instance_ref = self.__instance_dict[scope]
#            if instance_ref is None:
#                raise RuntimeError("invalid scope")
#            elif (instance := instance_ref()) is not None:
#                return instance
#
#        instance = super().__call__(scope, *args, **kwargs)
#        self.__instance_dict[scope] = ref(instance)
#        return instance
#
#    def _invalidate_scope(self, scope):
#        self.__instance_dict[scope] = None
#
#    def _get_instance(self, scope):
#        instance_ref = self.__instance_dict.get(scope)
#        if instance_ref is not None:
#            return instance_ref()
#
#class ScopedSingleton(metaclass=ScopedSingletonMeta):
#    __slots__ = ('__weakref__', '_scope')
#
#    def __init__(self, scope):
#        self._scope = scope
#
#    @classmethod
#    def _invalidate_scope(cls, scope):
#        instance = cls._get_instance(scope)
#        if instance is not None:
#            instance._scope = None
#        type(cls)._invalidate_scope(cls, scope)
#
#    @staticmethod
#    def _scope_valid(method):
#        """A method decorator that raises an error if the scope is invalid."""
#        @wraps(method)
#        def wrapper(self, /, *args, **kwargs):
#            if self._scope is None:
#                raise RuntimeError("invalid scope")
#            return method(self, *args, **kwargs)
#        return wrapper
