from typing import Any, Literal

import numpy as np
from pydantic import BaseModel
from ruamel.yaml import CommentedMap

from .utils import set_field

#########
# types #
#########

distributions = ["constant", "normal", "binomial"]


class Distribution(BaseModel):
    type: Literal[tuple(distributions)] = "constant"  # type: ignore


class Constant(Distribution):
    value: float = 0

    _set_type = set_field("type", "constant")


class Normal(Distribution):
    mu: float = 0
    sigma: float = 1

    _set_type = set_field("type", "normal")


class Binomial(Distribution):
    n: int = 1
    p: float = 0.5

    _set_type = set_field("type", "binomial")


############
# external #
############


def parse_distribution(distribution: dict[str, Any] | None) -> Distribution:
    if distribution is None or "type" not in distribution:
        raise ValueError()
    else:
        if distribution["type"] == "constant":
            return Constant(**distribution)
        elif distribution["type"] == "normal":
            return Normal(**distribution)
        elif distribution["type"] == "binomial":
            return Binomial(**distribution)
        else:
            raise NotImplementedError()


def generate_values(
    n: int, distribution: Distribution, rng: np.random.Generator
) -> list[float]:
    """
    Generates values from the given distribution.

    Parameters
    ----------
    n : int
        Number of values to return
    distribution : Distribution
        Distribution to use
    rng: np.random.Generator
        Random number generator to use

    Returns
    -------
    list[float]
        Generated values
    """
    if isinstance(distribution, Constant):
        return generate_constant(n, distribution, rng)
    elif isinstance(distribution, Normal):
        return generate_normal(n, distribution, rng)
    elif isinstance(distribution, Binomial):
        return generate_binomial(n, distribution, rng)
    else:
        raise NotImplementedError()


def add_distribution_comments(distribution: Distribution) -> CommentedMap:
    distribution_ = CommentedMap(distribution.dict())
    distribution_.yaml_add_eol_comment(
        f"Type of the distribution ({', '.join(distributions)})",
        "type",
    )
    if isinstance(distribution, Constant):
        distribution_ = add_constant_comments(distribution_)
    elif isinstance(distribution, Normal):
        distribution_ = add_normal_comments(distribution_)
    elif isinstance(distribution, Binomial):
        distribution_ = add_binomial_comments(distribution_)
    else:
        raise NotImplementedError()
    return distribution_


############
# internal #
############


def generate_constant(
    n: int, distribution: Constant, rng: np.random.Generator
) -> list[float]:
    return [distribution.value for _ in range(n)]


def generate_normal(
    n: int, distribution: Normal, rng: np.random.Generator
) -> list[float]:
    return list(rng.normal(distribution.mu, distribution.sigma, size=n))


def generate_binomial(
    n: int, distribution: Binomial, rng: np.random.Generator
) -> list[float]:
    return list(rng.binomial(n=distribution.n, p=distribution.p, size=n))


def add_constant_comments(distribution: CommentedMap) -> CommentedMap:
    distribution.yaml_add_eol_comment(
        "Value to give to each sample",
        "value",
    )
    return distribution


def add_normal_comments(distribution: CommentedMap) -> CommentedMap:
    distribution.yaml_add_eol_comment(
        "Mean of the distribution",
        "mu",
    )
    distribution.yaml_add_eol_comment(
        "Scale of the distribution",
        "sigma",
    )
    return distribution


def add_binomial_comments(distribution: CommentedMap) -> CommentedMap:
    distribution.yaml_add_eol_comment(
        "Number of possible successes",
        "n",
    )
    distribution.yaml_add_eol_comment(
        "Probability of success",
        "p",
    )
    return distribution
