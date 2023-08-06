from typing import Any, Dict, Hashable, Iterator, KeysView, Tuple, ValuesView

from .utils import Sentinel, iterable_cache


__all__ = ["Definition"]

_ignore = {
    "__module__",
    "__qualname__",
    "__doc__",
    "__annotations__",
    "__new__",
    "__classcell__",
}

_internal = {
    "_key2value_map_",
    "_value2key_map_",
    "_unique_",
    "_default_key_",
    "_default_value_",
}


class DefinitionMeta(type):
    def __new__(
        cls,
        clss: str,
        bases: Tuple[type],
        classdict: Dict[str, Any],
        *,
        default_key: str = Sentinel,
        default_value: Any = Sentinel,
        unique: bool = True,
    ):
        _key_to_baseclass_: Dict[str, type] = {}
        _key2value_map_: Dict[str, Any] = {}
        _value2key_map_: Dict[Any, str] = {}
        for base in bases:
            for key, value in getattr(base, "_key2value_map_", {}).items():

                if unique and not isinstance(value, Hashable):
                    raise ValueError(
                        f"'{value}' is not hashable, and thus cannot be used for uniquely-valued Definitions."
                    )

                if key in _key2value_map_:
                    raise ValueError(f"'{_key_to_baseclass_[key].__name__}' and '{base.__name__}' both defined '{key}'")

                if unique and value in _value2key_map_:
                    raise ValueError(f"'{_value2key_map_[value]}' and '{key}' have the same value: {value}")

                _key_to_baseclass_[key] = base
                _key2value_map_[key] = value
                if unique:
                    _value2key_map_[value] = key

        _new_class_ = super().__new__(cls, clss, bases, classdict)
        _new_class_._key2value_map_: Dict[str, Any] = _key2value_map_  # type: ignore
        _new_class_._value2key_map_: Dict[Any, str] = _value2key_map_  # type: ignore
        _new_class_._unique_: bool = unique  # type: ignore
        _new_class_._default_key_: str = default_key  # type: ignore
        _new_class_._default_value_: Any = default_value  # type: ignore

        for key, value in classdict.items():
            if key in _ignore:
                continue

            if unique and not isinstance(value, Hashable):
                raise ValueError(f"'{value}' is not hashable, and thus cannot be used for uniquely-valued Definitions.")

            if key in _new_class_._key2value_map_:
                raise ValueError(f"'{_key_to_baseclass_[key].__name__}' already defined '{key}'")

            if unique and value in _new_class_._value2key_map_:
                raise ValueError(f"'{_new_class_._value2key_map_[value]}' and '{key}' have the same value: {value}")

            _new_class_._key2value_map_[key] = value
            if unique:
                _new_class_._value2key_map_[value] = key

        return _new_class_

    def __setattr__(cls, key: Any, value: Any) -> None:
        # Allow specific attributes to be set once
        if key in _internal and key not in cls.__dict__:
            return super().__setattr__(key, value)

        raise AttributeError("Definition cannot be changed once created.")

    def __delattr__(cls, key: Any) -> None:
        raise AttributeError("Definition cannot be changed once created.")

    def __getitem__(cls, key: Any) -> Any:
        try:
            return cls._key2value_map_[key]
        except KeyError as error:
            if cls._default_value_ is not Sentinel:
                return cls._default_value_
            raise error

    def __call__(cls, value: Any = Sentinel) -> str:  # type: ignore
        if value is Sentinel:
            raise TypeError("Definition should not be instantiated.")

        if not cls._unique_:
            raise TypeError("Non unique-valued Definitions do not support reverse lookups.")

        try:
            return cls._value2key_map_[value]
        except KeyError as error:
            if cls._default_key_ is not Sentinel:
                return cls._default_key_
            raise error

    def __contains__(cls, item: Any) -> bool:
        return item in cls.values()  # pylint: disable=no-value-for-parameter

    def __str__(cls) -> str:
        return "{" + ", ".join([f"{key}={value}" for key, value in cls._key2value_map_.items()]) + "}"

    def __len__(cls) -> int:
        return len(cls._key2value_map_)

    def __iter__(cls) -> "DefinitionMeta":  # pylint: disable=non-iterator-returned
        return cls

    @iterable_cache(provider="values")
    def __next__(cls, keys: Iterator[str]) -> str:
        return next(keys)

    def keys(cls) -> KeysView[str]:
        """All definition keys in the Definition."""
        return cls._key2value_map_.keys()

    def values(cls) -> ValuesView[Any]:
        """All definition values in the Definition."""
        return cls._key2value_map_.values()


class Definition(metaclass=DefinitionMeta):
    r"""Create Definitions by subclassing this class.

    You can use the following class-level keywork arguments
    to change how the Definition behaves:

                  Arguments go here↴
    class MyDefinition(Definition, key=...):
        ...

    default_key: str — When no key is for a given value is found,
                       return this instead of raising a KeyError.
    default_value: Any — When no value is for a given key is found,
                         return this instead of raising a KeyError.
    unique: bool — By default, all keys and values in a definition have
                   to be unique. You can set unique=False to disable this,
                   but it also disables reverse lookup with values.
    """
