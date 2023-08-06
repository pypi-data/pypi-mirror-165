from dotenv import dotenv_values
from typing import Any, Optional


class Environment:
    def __init__(self, env_path: str = '.env'):
        env_values = self._get_env_values(env_path=env_path)
        self._set_attributes(env_values=env_values)
        del env_values

    @staticmethod
    def _get_env_values(env_path: str) -> dict:
        return dict(dotenv_values(dotenv_path=env_path))

    def _set_attributes(self, env_values: dict) -> None:
        for key in env_values:
            object.__setattr__(self, key.lower(), env_values.get(key))

    def __getattribute__(self, key: str) -> Any:
        return object.__getattribute__(self, key.lower())

    def __setattr__(self, key: str, value: Any) -> None:
        object.__setattr__(self, key.lower(), value)

    def __getattr__(self, key: str) -> Optional[Any]:
        try:
            return object.__getattribute__(self, key.lower())
        except AttributeError:
            return None

    def __delattr__(self, key: str) -> None:
        object.__delattr__(self, key.lower())

    def __getitem__(self, key: str) -> Optional[Any]:
        return self.__getattr__(key=key)

    def __setitem__(self, key: str, value: Any) -> None:
        object.__setattr__(self, key.lower(), value)

    def __iter__(self) -> iter:
        return iter(self.__dict__.__iter__())

    def __repr__(self) -> str:
        return f'<{type(self).__module__}.{type(self).__qualname__}> object at {hex(id(self))}'

    def __str__(self) -> str:
        return str(self.__dict__)

    def __len__(self) -> int:
        return len(self.__dict__)

    def keys(self) -> list:
        return list(self.__dict__.keys())

    def values(self) -> list:
        return list(self.__dict__.values())

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        value = self.__getattr__(key=key)
        return value if value else default

    @property
    def __version__(self) -> str:
        return '1.0.0'
