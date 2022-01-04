from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _typeshed import OpenTextMode

import importlib
import inspect
from collections import defaultdict
from typing import (Callable, Dict, Iterable, List, Optional, Tuple, Type,
                    TypeVar)
from warnings import warn

from .json_context import json_read

T = TypeVar("T")
Instance = TypeVar("Instance")
HookType = Callable[[Type[T], str], None]


class Error(Exception):
    pass


class RegistrationError(Error):
    pass


class Registrable:
    """
    Modified from ``https://github.com/epwalsh/python-registrable`` under its licence `Apache 2.0`.
    """

    _registry: Dict[Type, Dict[str, Type]] = defaultdict(dict)
    _hooks: Optional[List[HookType]] = None

    default_implementation: Optional[str] = None
    """
    Optional name of default implementation. If specified, the default will be listed
    first in :func:`registrable.Registrable.list_available`.
    """

    @classmethod
    def register(
        cls: Type[T],
        name: str,
        override: bool = False,
        hooks: Optional[List[HookType]] = None,
    ):
        """Class decorator for registering a subclass.

        Args:
            cls (Type[T]): register class
            name (str): The name to register the subclass under.
            override (bool, optional): If ``name`` is already registered a :class:`registrable.exceptions.RegistrationError` will be raised
            unless this is set to ``True``. Defaults to False.
            hooks (Optional[List[HookType]], optional): Hooks to run when the subclass is registered.. Defaults to None.

        Raises:
            RegistrationError
        """

        registry = Registrable._registry[cls]
        default_hooks = cls._hooks or []  # type: ignore

        def add_subclass_to_registry(subclass: Type[T]):
            if not inspect.isclass(subclass) or not issubclass(subclass, cls):
                raise RegistrationError(
                    f"Cannot register {subclass.__name__} as {name}; "
                    f"{subclass.__name__} must be a subclass of {cls.__name__}"
                )
            # Add to registry.
            # If name already registered, warn if overriding or raise an error if override not allowed.
            if name in registry:
                if not override:
                    raise RegistrationError(
                        f"Cannot register {subclass.__name__} as {name}; "
                        f"name already in use for {registry[name].__name__}"
                    )
                else:
                    warn(f"Overriding {name} in {cls.__name__} registry")
            registry[name] = subclass
            for hook in default_hooks + (hooks or []):
                hook(subclass, name)
            return subclass

        return add_subclass_to_registry

    @classmethod
    def hook(cls, hook: HookType):
        """
        Function decorator for adding a default hook to a registrable base class.
        """
        if not cls._hooks:
            cls._hooks = []
        cls._hooks.append(hook)
        return hook

    @classmethod
    def by_name(cls: Type[T], name: str) -> Type[T]:
        """Get a subclass by its registered name, or its fully qualified class name.

        Args:
            cls (Type[T]): class to register
            name (str): registration name

        Raises:
            RegistrationError

        Returns:
            Type[T]: The subclass registered under ``name``.
        """
        if name in Registrable._registry[cls]:
            return Registrable._registry[cls][name]
        elif "." in name:
            # This might be a fully qualified class name, so we'll try importing its "module"
            # and finding it there.
            parts = name.split(".")
            submodule = ".".join(parts[:-1])
            class_name = parts[-1]

            try:
                module = importlib.import_module(submodule)
            except ModuleNotFoundError:
                raise RegistrationError(
                    f"tried to interpret {name} as a path to a class "
                    f"but unable to import module {submodule}"
                )

            try:
                maybe_subclass = getattr(module, class_name)
            except AttributeError:
                raise RegistrationError(
                    f"tried to interpret {name} as a path to a class "
                    f"but unable to find class {class_name} in {submodule}"
                )

            if not inspect.isclass(maybe_subclass) or not issubclass(
                maybe_subclass, cls
            ):
                raise RegistrationError(
                    f"tried to interpret {name} as a path to a class "
                    f"but {class_name} is not a subclass of {cls.__name__}"
                )

            # Add subclass to registry and return it.
            Registrable._registry[cls][name] = maybe_subclass
            return maybe_subclass
        else:
            # is not a qualified class name
            raise RegistrationError(
                f"{name} is not a registered name for {cls.__name__}."
            )

    @classmethod
    def from_dict(cls: Type[T], json_dict: Dict, *args, **kwargs) -> Type[Instance]:
        """Get instance with ``dictionary`` initialization.

        Args:
            cls (Type[T]): subclass which is registered.
            json_path (str): ``path/to/json``. The key ``type`` should be assigned in ``json`` and the value should be registered by its name.

        Returns:
            Type[T]: incetance of subclass
        """
        json_dict_tmp = json_dict.copy()
        subcls = cls.by_name(json_dict_tmp.pop('type'))  # type: ignore
        instance = subcls(*args, **kwargs, **json_dict_tmp)
        return instance

    @classmethod
    def from_json(
        cls: Type[T],
        json_path: str,
        mode: Optional[OpenTextMode] = 'r',
        buffering: Optional[int] = -1,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
        newline: Optional[str] = None,
        closefd: Optional[bool] = True,
        opener: Optional[Callable] = None,
        *args,
        **kwargs
    ) -> Type[Instance]:
        """Get instance with ``json`` initialization.

        Args:
            cls (Type[T]): subclass which is registered.
            json_path (str): ``path/to/json``. The key ``type`` should be assigned in ``json`` and the value should be registered by its name.

        Returns:
            Type[T]: incetance of subclass
        """
        with json_read(
            json_path,
            mode=mode,
            buffering=buffering,
            encoding=encoding,
            errors=errors,
            newline=newline,
            closefd=closefd,
            opener=opener,
        ) as json_dict:
            instance = cls.from_dict(  # type: ignore
                json_dict, *args, **kwargs)
        return instance

    @classmethod
    def list_available(cls: Type[T]) -> List[str]:
        """
        List all registered subclasses.
        If ``cls.default_implementation`` is specified, it will be first in the list.
        """
        keys = list(Registrable._registry[cls].keys())
        default = cls.default_implementation  # type: ignore

        if default is None:
            return keys
        if default not in keys:
            raise RegistrationError(
                f"Default implementation {default} is not registered"
            )
        return [default] + [k for k in keys if k != default]

    @classmethod
    def is_registered(cls: Type[T], name: str) -> bool:
        """
        Returns True if ``name`` is a registered name.
        """
        return name in Registrable._registry[cls]

    @classmethod
    def iter_registered(cls: Type[T]) -> Iterable[Tuple[str, Type[T]]]:
        """
        Iterate through the registered names and subclasses.
        """
        return Registrable._registry[cls].items()
