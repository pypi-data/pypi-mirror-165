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
from .skills import Skill
from .utils import clip_0_1, load_print, parse_config, set_seed_if_missing

#########
# types #
#########


class Student(BaseModel):
    id: int
    slip: float
    guess: float
    learning_rate: float
    forget_rate: float
    skills: dict[int, float]


class Config(BaseModel):
    n: int = 4000
    binary_learning: bool = False
    n_skills: Distribution = Constant(value=3)
    skill_mastery: Distribution = Constant(value=1)
    slip: Distribution = Constant(value=0)
    guess: Distribution = Constant(value=0)
    learning_rate: Distribution = Constant(value=0.1)
    forget_rate: Distribution = Constant(value=0)
    seed: int = 0

    _parse_n_skills = parse_config("n_skills", parse_distribution)
    _parse_skill_mastery = parse_config("skill_mastery", parse_distribution)
    _parse_slip = parse_config("slip", parse_distribution)
    _parse_guess = parse_config("guess", parse_distribution)
    _parse_learning_rate = parse_config("learning_rate", parse_distribution)
    _parse_forget_rate = parse_config("forget_rate", parse_distribution)
    _set_seed = set_seed_if_missing("seed")

    class Config:
        validate_assignment = True


############
# external #
############


def generate(
    config: Config | list[Config], skills: list[Skill], echo: bool = True
) -> list[Student]:
    load_print("Generating students...", echo=echo)
    if isinstance(config, Config):
        (
            slips,
            guesses,
            learning_rates,
            forget_rates,
            skills_,
            skill_masteries,
        ) = generate_params(config, skills)
    else:
        (
            slips,
            guesses,
            learning_rates,
            forget_rates,
            skills_,
            skill_masteries,
        ) = (
            [],
            [],
            [],
            [],
            [],
            [],
        )
        for config_ in config:
            (
                slips_,
                guesses_,
                learning_rates_,
                forget_rates_,
                skills__,
                skill_masteries_,
            ) = generate_params(config_, skills)
            slips = [*slips, *slips_]
            guesses = [*guesses, *guesses_]
            learning_rates = [*learning_rates, *learning_rates_]
            forget_rates = [*forget_rates, *forget_rates_]
            skills_ = [*skills_, *skills__]
            skill_masteries = [*skill_masteries, *skill_masteries_]

    return [
        Student(
            id=i,
            slip=slip,
            guess=guess,
            learning_rate=learning_rate,
            forget_rate=forget_rate,
            skills={
                skill: mastery for skill, mastery in zip(skills__, masteries)
            },
        )
        for i, (
            slip,
            guess,
            learning_rate,
            forget_rate,
            skills__,
            masteries,
        ) in enumerate(
            zip(
                slips,
                guesses,
                learning_rates,
                forget_rates,
                skills_,
                skill_masteries,
            )
        )
    ]


def add_comments(
    config: Config | list[Config],
) -> CommentedMap | list[CommentedMap]:
    if isinstance(config, Config):
        config_ = CommentedMap(config.dict())
        config_.yaml_add_eol_comment(
            "Number of students",
            "n",
        )
        config_.yaml_add_eol_comment(
            "If a skill is binary, learned or not",
            "binary_learning",
        )
        config_.yaml_add_eol_comment(
            "Distribution of the number of skills per student",
            "n_skills",
        )
        config_["n_skills"] = add_distribution_comments(config.n_skills)
        config_.yaml_add_eol_comment(
            "Distribution of the skill mastery for each student skill",
            "skill_mastery",
        )
        config_["skill_mastery"] = add_distribution_comments(
            config.skill_mastery
        )
        config_.yaml_add_eol_comment(
            "Distribution of the student slip parameter",
            "slip",
        )
        config_["slip"] = add_distribution_comments(config.slip)
        config_.yaml_add_eol_comment(
            "Distribution of the student guess parameter",
            "guess",
        )
        config_["guess"] = add_distribution_comments(config.guess)
        config_.yaml_add_eol_comment(
            "Distribution of the student learning rate parameter",
            "learning_rate",
        )
        config_["learning_rate"] = add_distribution_comments(
            config.learning_rate
        )
        config_.yaml_add_eol_comment(
            "Distribution of the student forget rate parameter",
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


def generate_params(
    config: Config, skills: list[Skill]
) -> tuple[
    list[float],
    list[float],
    list[float],
    list[float],
    list[list[int]],
    list[list[float]],
]:
    rng = np.random.default_rng(config.seed)
    skill_ids = [skill.id for skill in skills]
    n_skills = [
        min(len(skills), max(1, int(val)))
        for val in generate_values(config.n, config.n_skills, rng)
    ]
    skills_ = [
        list(rng.choice(skill_ids, size=n, replace=False)) for n in n_skills
    ]
    skill_masteries_ = clip_0_1(
        generate_values(sum(n_skills), config.skill_mastery, rng)
    )
    skill_masteries = [
        skill_masteries_[sum(n_skills[:i]) : sum(n_skills[: i + 1])]
        for i in range(len(n_skills))
    ]
    slips = clip_0_1(generate_values(config.n, config.slip, rng))
    guesses = clip_0_1(generate_values(config.n, config.guess, rng))
    learning_rates = clip_0_1(
        generate_values(config.n, config.learning_rate, rng)
    )
    forget_rates = clip_0_1(generate_values(config.n, config.forget_rate, rng))
    return (
        slips,
        guesses,
        learning_rates,
        forget_rates,
        skills_,
        skill_masteries,
    )
