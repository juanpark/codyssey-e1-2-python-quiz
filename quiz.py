class Quiz:
    def __init__(self, question: str, choices: list[str], answer: int):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self):
        print(self.question)
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def is_correct(self, choice_number: int):
        return self.answer == choice_number


if __name__ == '__main__':
    q = Quiz("What's the answer?", ["foo", "bar", "baz", "qux"], 4)
    q.display()
    print(q.is_correct(1))
    print(q.is_correct(4))
