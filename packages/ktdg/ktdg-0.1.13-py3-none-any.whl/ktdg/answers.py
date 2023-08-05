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
from .questions import Question
from .skills import Skill
from .students import Student
from .utils import (
    create_skill_vector,
    load_print,
    parse_config,
    set_seed_if_missing,
)

#########
# types #
#########


class Answer(BaseModel):
    id: int
    student: int
    question: int
    timestamp: int
    correct: bool
    p_correct: float
    state: dict[int, float]


class Config(BaseModel):
    wrong_answer_adjustment: float = 0
    guess_adjustment: float = 0
    mastery_importance: float = 1
    n_per_student: Distribution = Constant(value=50)
    max_repetitions: int = 1
    can_repeat_correct: bool = False
    seed: int = 0

    _parse_n_per_student = parse_config("n_per_student", parse_distribution)
    _set_seed = set_seed_if_missing("seed")

    class Config:
        validate_assignment = True


############
# external #
############


def generate(
    config: Config,
    students: list[Student],
    questions: list[Question],
    skills: list[Skill],
    echo: bool = True,
) -> list[list[Answer]]:
    load_print("Generating answers...", echo=echo)
    rng = np.random.default_rng(config.seed)
    skill_difficulties = np.array([skill.difficulty for skill in skills])
    skill_forget_rates = np.array([skill.forget_rate for skill in skills])
    answers: list[list[Answer]] = []
    for i, student in enumerate(students):
        load_print(
            "Generating answers...", symbol=f"{i+1}/{len(students)}", echo=echo
        )
        answers.append(
            generate_student_answers(
                config,
                student,
                questions,
                skill_difficulties,
                skill_forget_rates,
                rng,
            )
        )
    i = 0
    for answers_ in answers:
        for answer in answers_:
            answer.id = i
            i += 1
    return answers


def add_comments(config: Config) -> CommentedMap:
    config_ = CommentedMap(config.dict())
    config_.yaml_add_eol_comment(
        "How much should the learning be scaled when the answer is wrong",
        "wrong_answer_adjustment",
    )
    config_.yaml_add_eol_comment(
        "How much should the learning be scaled proportional to guess value",
        "guess_adjustment",
    )
    config_.yaml_add_eol_comment(
        "How much the skill mastery should be scaled by in the exponential",
        "mastery_importance",
    )
    config_.yaml_add_eol_comment(
        "Number of answers by student",
        "n_per_student",
    )
    config_["n_per_student"] = add_distribution_comments(config.n_per_student)
    config_.yaml_add_eol_comment(
        "Maximum number of times a question can be repeated "
        + "(to allow unlimited, set to 0)",
        "max_repetitions",
    )
    config_.yaml_add_eol_comment(
        "If a correctly answered question can be asked again",
        "can_repeat_correct",
    )
    config_.yaml_add_eol_comment(
        "random seed to use (set to 0 to have new seed)", "seed"
    )
    return config_


############
# internal #
############


def generate_student_answers(
    config: Config,
    student: Student,
    questions: list[Question],
    skill_difficulties: np.ndarray,
    skill_forget_rates: np.ndarray,
    rng: np.random.Generator,
) -> list[Answer]:
    n_skills = skill_difficulties.shape[0]
    n_questions = min(
        len(questions), int(generate_values(1, config.n_per_student, rng)[0])
    )
    skill_state = create_skill_vector(student.skills, n_skills)

    answers: list[Answer] = []
    for i in range(n_questions):
        question = choose_question(
            answers,
            questions,
            config.max_repetitions,
            config.can_repeat_correct,
            rng,
        )
        question_ = create_skill_vector(question.skills, n_skills)
        p_correct = compute_p_correct(
            skill_state,
            question_,
            student,
            question,
            config.mastery_importance,
        )
        correct = bool(rng.binomial(1, p_correct))
        skill_state = update_skill_state(
            skill_state,
            question_,
            skill_difficulties,
            skill_forget_rates,
            correct,
            student,
            question,
            config.wrong_answer_adjustment,
            config.guess_adjustment,
        )
        answers.append(
            Answer(
                id=0,
                student=student.id,
                question=question.id,
                timestamp=i,
                correct=correct,
                p_correct=p_correct,
                state={i: v for i, v in enumerate(skill_state) if v},
            )
        )
    return answers


def choose_question(
    answers: list[Answer],
    questions: list[Question],
    max_repetitions: int,
    can_repeat_correct: bool,
    rng: np.random.Generator,
) -> Question:
    freqs = [
        len([answer for answer in answers if answer.question == question.id])
        for question in questions
    ]
    questions = [
        question
        for question, freq in zip(questions, freqs)
        if max_repetitions == 0 or freq < max_repetitions
    ]
    if not can_repeat_correct:
        answered_correctly = {
            answer.question for answer in answers if answer.correct
        }
        questions = [
            question
            for question in questions
            if question.id not in answered_correctly
        ]
    if not len(questions):
        raise RuntimeError("There are no questions left to ask.")
    return rng.choice(questions)  # type: ignore


def compute_p_correct(
    student_skills: np.ndarray,
    question_skills: np.ndarray,
    student: Student,
    question: Question,
    mastery_importance: float,
) -> float:
    slip, guess = compute_slip_and_guess(student, question)
    mastery = np.exp(
        mastery_importance
        * (np.dot(student_skills, question_skills) - question.difficulty)
    )
    return min(guess + (1 - slip) * mastery / (1 + mastery), 1)


def update_skill_state(
    student_skills: np.ndarray,
    question_skills: np.ndarray,
    skill_difficulties: np.ndarray,
    skill_forget_rates: np.ndarray,
    correct: bool,
    student: Student,
    question: Question,
    wrong_answer_adjustment: float,
    guess_adjustment: float,
) -> np.ndarray:
    _, guess = compute_slip_and_guess(student, question)
    guess_adjustment = (1 - guess_adjustment) * (1 - guess)
    forget_rates = 1 - np.sqrt(
        (1 - skill_forget_rates) * (1 - student.forget_rate)
    )
    return (
        student_skills * (1 - forget_rates)
        + student.learning_rate
        * guess_adjustment
        * question_skills
        * (0.5 + question.difficulty)
        * (1 - wrong_answer_adjustment * (1 - correct))
        * (1 - skill_difficulties)
    ).clip(0, 1)


def compute_slip_and_guess(
    student: Student, question: Question
) -> tuple[float, float]:
    slip = 1 - np.sqrt((1 - student.slip) * (1 - question.slip))
    guess = 1 - np.sqrt((1 - student.guess) * (1 - question.guess))
    return slip, guess
