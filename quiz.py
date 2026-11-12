"""Quiz entity: a single question with its choices and correct answer and hint."""
from __future__ import annotations


class Quiz:
    """One quiz question.

    Attributes:
        question: the question text.
        choices: a list of 4 answer options (indexed 0-3).
        answer: the correct choice as a number 1-4, so choices[answer-1] is
            the correct option's text. (answer stays in human 1-4 space; the
            only -1 is when indexing into choices.)
        hint: optional hint text, or None.
    """

    def __init__(self, question: str, choices: list[str], answer: int, hint: str | None = None):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def display(self):
        """Print the question, then the 4 choices numbered 1-4."""
        print(self.question)
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def is_correct(self, choice_number: int):
        """Return True if the given 1-4 choice number is the correct answer."""
        return self.answer == choice_number

    def to_dict(self) -> dict:
        """Return a dict representation of the quiz."""
        return {
            "question": self.question,
            "choices": self.choices,  # already a list[str] --> safe for JSON
            "answer": self.answer,  # int --> safe for JSON
            "hint": self.hint  # str or None --> safe for JSON
        }

    @classmethod  # makes 1st arg the CLASS, not an instance
    def from_dict(cls, data: dict) -> Quiz:
        """Return a Quiz instance from a dict representation of the quiz."""
        return cls( # cls is Quiz --> this is Quiz(...)
            question=data["question"],  # [] is core field; missing means corrupt (let it raise)
            choices=data["choices"],
            answer=data["answer"],
            hint=data.get("hint")  # .get() is optional; missing --> None, no crash
        )


if __name__ == '__main__':
    q = Quiz("What's the answer?", ["foo", "bar", "baz", "qux"], 4)
    q.display()
    print(q.is_correct(1))
    print(q.is_correct(4))

    a = q.to_dict()
    b = Quiz.from_dict(a)
    print(q.to_dict() == b.to_dict())
