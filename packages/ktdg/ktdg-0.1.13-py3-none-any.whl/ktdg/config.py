from pathlib import Path

from pydantic import BaseModel
from ruamel.yaml import YAML, CommentedMap

from . import answers as answers_
from . import questions as questions_
from . import skills as skills_
from . import students as students_

#########
# types #
#########


class Config(BaseModel):
    skills: skills_.Config | list[skills_.Config] = skills_.Config()
    questions: questions_.Config | list[
        questions_.Config
    ] = questions_.Config()
    students: students_.Config | list[students_.Config] = students_.Config()
    answers: answers_.Config = answers_.Config()


############
# external #
############


def read_config(config: Path | None = None) -> Config:
    if config is None or not config.exists():
        return Config()
    else:
        yaml = YAML()
        with open(config, "r") as f:
            config_ = Config(**yaml.load(f))
        return config_


def save_config(config: Config, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    yaml = YAML()
    with open(path, "w") as f:
        yaml.dump(add_comments(config), f)


############
# internal #
############


def add_comments(config: Config) -> CommentedMap:
    config_ = CommentedMap(config.dict())
    config_["skills"] = skills_.add_comments(config.skills)
    config_["questions"] = questions_.add_comments(config.questions)
    config_["students"] = students_.add_comments(config.students)
    config_["answers"] = answers_.add_comments(config.answers)
    return config_
