import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from . import answers as answers_
from . import questions as questions_
from . import skills as skills_
from . import students as students_
from .config import Config
from .utils import done_print

#########
# types #
#########


class Data(BaseModel):
    skills: list[skills_.Skill]
    students: list[students_.Student]
    questions: list[questions_.Question]
    answers: list[answers_.Answer]


############
# external #
############


def generate(
    config: Config, as_dict: bool = False, echo: bool = True
) -> Data | dict[str, Any]:
    skills = skills_.generate(config.skills, echo=echo)
    students = students_.generate(config.students, skills, echo=echo)
    questions = questions_.generate(config.questions, skills, echo=echo)
    student_answers = answers_.generate(
        config.answers, students, questions, skills, echo=echo
    )
    answers = [aa for a in student_answers for aa in a]
    data = Data(
        skills=skills, students=students, questions=questions, answers=answers
    )
    done_print("Generated data.", echo=echo)
    if as_dict:
        return data.dict()
    else:
        return data


def save_data(data: Data | dict[str, Any]) -> None:
    if isinstance(data, Data):
        data = data.dict()
    with open(Path() / "data.json", "w") as f:
        json.dump(data, f, indent=2)
