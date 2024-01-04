"""
Module used to add extensions to add extensions
to TkClassWizard.
"""
from typing import Callable, TypeVar, Union
from inspect import isclass
from functools import wraps

from .doc import doc_category, DOCUMENTATION_MODE


T = TypeVar('T')


class Extension:
    """
    The extension class.

    Parameters
    ----------
    name: str
        The name of the extension.
    version: str
        The (semantic) version of the extension.
    loader: Callable
        The extension loader, which is called at every extended object initialization / call.
        See :func:`tkclasswiz.extensions.extendable` for more information about how it is called.
    """
    def __init__(self, name: str, version: str, loader: Callable[[T], None]) -> None:
        self._name = name
        self._version = version
        self._loader = loader

    def __repr__(self) -> str:
        return f"Extension(name={self._name}, version={self._version}, loader={self._loader.__name__})"

    def __call__(self, *args: T, **kwargs: T) -> None:
        return self._loader(*args, **kwargs)

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @property
    def loader(self):
        return self._loader


@doc_category("Extensions")
def extendable(obj: Union[T, list]) -> T:
    """
    Decorator that makes the obj extendable.

    It wraps the ``obj``, which is a class or a function, into an extension object.
    The extension object will adds 3 methods to the original class or function:

    - ``register_pre_extension``
    - ``register_post_extension``
    - ``get_extensions``
    
    The ``get_extensions`` method just returns the list of registered 
    extensions (:class:`tkclasswiz.extensions.Extension`).

    The ``register_pre_extension`` and ``register_post_extension`` methods allow users to extend
    the functionality of original tkclass wiz classes or functions.
    They accept the extension (:class:`tkclasswiz.extensions.Extension`) parameter.

    Pre-extensions (``register_pre_extension``) get activated / called before the original ``__init__`` method / 
    before the original function and accept the ``loader`` of the extension must accept the same arguments
    as the original ``__init__`` method / original function.

    Post-extensions differ a bit if the thing being extended is a class  or a function.
    They both have in common that they get activated after the original ``__init__`` method call / original function
    call, but they differ in the arguments they receive:

    - In the case of the extended is a class,
      the extension ``loader`` accepts the same arguments as the ``__init__`` method receives.
    - In the case of the extended is a function,
      the extension ``loader`` accepts the same arguments as the original function and an additional parameter,
      which is the result of the original function call. The result parameter is passed to the ``loader`` as the
      last positional argument.


    Parameters
    ---------------
    obj: T
        Function or a class that can be extended.
    """

    if DOCUMENTATION_MODE:
        return obj

    if isclass(obj):
        @wraps(obj, updated=[])
        class ExtendableClass(obj):
            __reg_post_ext__ = []
            __reg_pre_ext__ = []

            def __init__(self, *args, **kwargs):
                for extension in ExtendableClass.__reg_pre_ext__:
                    extension(self, *args, **kwargs)

                super().__init__(*args, **kwargs)

                extension: Extension
                for extension in ExtendableClass.__reg_post_ext__:
                    extension(self, *args, **kwargs)

            @classmethod
            def register_pre_extension(cls, extension: Extension):
                cls.__reg_pre_ext__.append(extension)

            @classmethod
            def register_post_extension(obj, extension: Extension):
                obj.__reg_post_ext__.append(extension)

            @classmethod
            def get_extensions(obj):
                return obj.__reg_pre_ext__, obj.__reg_post_ext__[:]

        return ExtendableClass
    else:
        class ExtendableFunction:
            __reg_post_ext__ = []
            __reg_pre_ext__ = []

            def __init__(self, bind: object = None) -> None:
                self.bind = bind

            def __call__(self, *args, **kwargs):
                if self.bind is not None:
                    extra_args = (self.bind,)  # self reference
                else:
                    extra_args = ()

                for ext in ExtendableFunction.__reg_pre_ext__:
                    ext(*extra_args, *args, **kwargs)

                r = obj(*extra_args, *args, **kwargs)
                
                for ext in ExtendableFunction.__reg_post_ext__:
                    r = ext(*extra_args, *args, r, **kwargs)

                return r

            def __get__(self, instance, cls):
                # Bind the wrapper callable object into a callable object "instance"
                return ExtendableFunction(instance)

            @classmethod
            def register_pre_extension(cls, extension: Extension):
                cls.__reg_pre_ext__.append(extension)

            @classmethod
            def register_post_extension(cls, extension: Extension):
                cls.__reg_post_ext__.append(extension)

            @classmethod
            def get_extensions(obj):
                return obj.__reg_pre_ext__, obj.__reg_post_ext__[:]

        return ExtendableFunction()
