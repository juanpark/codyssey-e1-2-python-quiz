"""Persistence layer: the only module that reads/writes state.json."""
import json
from quiz import Quiz
from default_data import default_quizzes


class Storage:
    """Reads and writes the quiz state to state.json (UTF-8)."""
    def __init__(self, path="state.json"):
        self.path = path
        self.source = None

    def save(self, quizzes):
        data = {"quizzes": [q.to_dict() for q in quizzes]} # object, not bare list
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            # ensure_ascii=False shows readable Hangeul

    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
            quizzes = [Quiz.from_dict(d) for d in data.get("quizzes", [])]
            self.source = "file"
            return quizzes
        except FileNotFoundError:
            self.source = "new"
            return default_quizzes()
        except (json.JSONDecodeError, KeyError, TypeError, AttributeError):
            self.source = "corrupt"
            return default_quizzes()
        # FileNotFoundError: no file, state.json, yet (first run, fresh clone)
        # json.JSONDecodeError: file exists but isn't valid JSON
        # KeyError: a dict is missing a core field
        # TypeError: the shape is wrong
        # AttributeError: valid JSON but wrong shape
