import random
import shutil
from typing import Any, Callable, Type

import numpy as np
from pydantic import BaseModel, validator


def load_print(text: str, symbol: str = "*", echo: bool = True) -> None:
    symbol = f"\033[1m[{symbol}]\033[0m"
    if echo:
        print(
            f"\r{symbol} {text}".ljust(shutil.get_terminal_size().columns),
            end="\r",
        )


def done_print(text: str, symbol: str = "+", echo: bool = True) -> None:
    symbol = f"\033[1m\033[92m[{symbol}]\033[0m"
    if echo:
        print(f"\r{symbol} {text}".ljust(shutil.get_terminal_size().columns))


def set_field(field: str, value: Any) -> Callable:
    def fct_(cls: Type[BaseModel], val: Any) -> Any:
        return value

    return validator(field, allow_reuse=True, always=True)(fct_)  # type: ignore # noqa


def set_seed_if_missing(field: str) -> Callable:
    def fct_(val: int) -> int:
        if val == 0:
            return random.randint(0, 100_000)  # nosec
        else:
            return val

    return validator(field, allow_reuse=True, always=True)(fct_)  # type: ignore # noqa


def parse_config(field: str, fct: Callable) -> Callable:
    def fct_(
        cls: Type[BaseModel], val: dict[str, Any] | BaseModel | None
    ) -> BaseModel:
        if isinstance(val, BaseModel):
            return val
        elif val is None:
            return fct()
        else:
            return fct(val)

    return validator(field, allow_reuse=True, always=True, pre=True)(fct_)  # type: ignore # noqa


def clip_0_1(values: list[float]) -> list[float]:
    return [min(max(v, 0), 1) for v in values]


def create_skill_vector(skills: dict[int, float], n_skills: int) -> np.ndarray:
    return np.array([skills.get(skill, 0) for skill in range(n_skills)])
