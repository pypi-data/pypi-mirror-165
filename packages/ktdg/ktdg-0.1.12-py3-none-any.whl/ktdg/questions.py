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


class Question(BaseModel):
    id: int
    difficulty: float
    slip: float
    guess: float
    skills: dict[int, float]


class Config(BaseModel):
    n: int = 50
    n_skills: Distribution = Constant(value=1)
    skill_mastery: Distribution = Constant(value=1)
    difficulty: Distribution = Constant(value=0.5)
    slip: Distribution = Constant(value=0)
    guess: Distribution = Constant(value=0)
    seed: int = 0

    _parse_n_skills = parse_config("n_skills", parse_distribution)
    _parse_skill_mastery = parse_config("skill_mastery", parse_distribution)
    _parse_difficulty = parse_config("difficulty", parse_distribution)
    _parse_slip = parse_config("slip", parse_distribution)
    _parse_guess = parse_config("guess", parse_distribution)
    _set_seed = set_seed_if_missing("seed")

    class Config:
        validate_assignment = True


############
# external #
############


def generate(
    config: Config | list[Config], skills: list[Skill], echo: bool = True
) -> list[Question]:
    load_print("Generating questions...", echo=echo)

    if isinstance(config, Config):
        (
            difficulties,
            slips,
            guesses,
            skills_,
            skill_masteries,
        ) = generate_params(config, skills)
    else:
        difficulties, slips, guesses, skills_, skill_masteries = (
            [],
            [],
            [],
            [],
            [],
        )
        for config_ in config:
            (
                difficulties_,
                slips_,
                guesses_,
                skills__,
                skill_masteries_,
            ) = generate_params(config_, skills)
            difficulties = [*difficulties, *difficulties_]
            slips = [*slips, *slips_]
            guesses = [*guesses, *guesses_]
            skills_ = [*skills_, *skills__]
            skill_masteries = [*skill_masteries, *skill_masteries_]

    return [
        Question(
            id=i,
            difficulty=difficulty,
            slip=slip,
            guess=guess,
            skills={
                skill: mastery for skill, mastery in zip(skills__, masteries)
            },
        )
        for i, (difficulty, slip, guess, skills__, masteries) in enumerate(
            zip(difficulties, slips, guesses, skills_, skill_masteries)
        )
    ]


def add_comments(
    config: Config | list[Config],
) -> CommentedMap | list[CommentedMap]:
    if isinstance(config, Config):
        config_ = CommentedMap(config.dict())
        config_.yaml_add_eol_comment(
            "Number of questions",
            "n",
        )
        config_.yaml_add_eol_comment(
            "Distribution of the number of skills needed per question",
            "n_skills",
        )
        config_["n_skills"] = add_distribution_comments(config.n_skills)
        config_.yaml_add_eol_comment(
            "Distribution of the skill mastery for each question skill",
            "skill_mastery",
        )
        config_["skill_mastery"] = add_distribution_comments(
            config.skill_mastery
        )
        config_.yaml_add_eol_comment(
            "Distribution of the question difficulty",
            "difficulty",
        )
        config_["difficulty"] = add_distribution_comments(config.difficulty)
        config_.yaml_add_eol_comment(
            "Distribution of the question slip parameter",
            "slip",
        )
        config_["slip"] = add_distribution_comments(config.slip)
        config_.yaml_add_eol_comment(
            "Distribution of the question guess parameter",
            "guess",
        )
        config_["guess"] = add_distribution_comments(config.guess)
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
    list[float], list[float], list[float], list[list[int]], list[list[float]]
]:
    rng = np.random.default_rng(config.seed)
    skill_ids = [s.id for s in skills]
    n_skills = [
        min(len(skills), max(1, int(v)))
        for v in generate_values(config.n, config.n_skills, rng)
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
    difficulties = clip_0_1(generate_values(config.n, config.difficulty, rng))
    slips = clip_0_1(generate_values(config.n, config.slip, rng))
    guesses = clip_0_1(generate_values(config.n, config.guess, rng))
    return difficulties, slips, guesses, skills_, skill_masteries
