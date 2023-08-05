import numpy as np
from pydantic import BaseModel
from ruamel.yaml import CommentedMap

from .distributions import (
    Constant,
    Distribution,
    add_distribution_comments,
    generate_values,
    parse_distribution,
)
from .utils import clip_0_1, load_print, parse_config, set_seed_if_missing

#########
# types #
#########


class Skill(BaseModel):
    id: int
    difficulty: float
    forget_rate: float


class Config(BaseModel):
    n: int = 5
    difficulty: Distribution = Constant(value=0)
    forget_rate: Distribution = Constant(value=0)
    seed: int = 0

    _parse_difficulty = parse_config("difficulty", parse_distribution)
    _parse_forget_rate = parse_config("forget_rate", parse_distribution)
    _set_seed = set_seed_if_missing("seed")

    class Config:
        validate_assignment = True


############
# external #
############


def generate(config: Config | list[Config], echo: bool = True) -> list[Skill]:
    load_print("Generating skills...", echo=echo)
    if isinstance(config, Config):
        difficulties, forget_rates = generate_params(config)
    else:
        difficulties, forget_rates = [], []
        for config_ in config:
            difficulties_, forget_rates_ = generate_params(config_)
            difficulties = [*difficulties, *difficulties_]
            forget_rates = [*forget_rates, *forget_rates_]

    return [
        Skill(id=i, difficulty=difficulty, forget_rate=forget_rate)
        for i, (difficulty, forget_rate) in enumerate(
            zip(difficulties, forget_rates)
        )
    ]


def add_comments(
    config: Config | list[Config],
) -> CommentedMap | list[CommentedMap]:
    if isinstance(config, Config):
        config_ = CommentedMap(config.dict())
        config_.yaml_add_eol_comment(
            "Number of skils",
            "n",
        )
        config_.yaml_add_eol_comment(
            "Distribution of the skill difficulty",
            "difficulty",
        )
        config_["difficulty"] = add_distribution_comments(config.difficulty)
        config_.yaml_add_eol_comment(
            "Distribution of the skill forget rate parameter",
            "forget_rate",
        )
        config_["forget_rate"] = add_distribution_comments(config.forget_rate)
        config_.yaml_add_eol_comment(
            "random seed to use (set to 0 to have new seed)", "seed"
        )
        return config_
    else:
        return [add_comments(c) for c in config]  # type: ignore


############
# internal #
############


def generate_params(config: Config) -> tuple[list[float], list[float]]:
    rng = np.random.default_rng(config.seed)
    difficulties = clip_0_1(generate_values(config.n, config.difficulty, rng))
    forget_rates = clip_0_1(generate_values(config.n, config.forget_rate, rng))
    return difficulties, forget_rates
