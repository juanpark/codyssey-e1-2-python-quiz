"""Persistence layer: the only module that reads/writes state.json."""
import json
import os
import shutil
from quiz import Quiz
from default_data import default_quizzes


class Storage:
    """Reads and writes the quiz state to state.json (UTF-8)."""
    def __init__(self, path="state.json"):
        self.path = path
        self.source = None
        self.history = []

    def save(self, quizzes, history, best_score):
        data = {
            "quizzes": [q.to_dict() for q in quizzes],
            "history": history,
            "best_score": best_score,
            # best_score is a DERIVED mirror of history, recomputed and written on
            # every save for schema compatibility. load() never reads it back --
            # history is the single source of truth, so the two can never drift.
        }  # object, not bare list
        try:
            # Write to a temp file, then atomically replace the real one. If the
            # process dies mid-write, state.json is never left half-written.
            tmp = self.path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                # ensure_ascii=False shows readable Hangeul
            os.replace(tmp, self.path)
        except (PermissionError, OSError) as error:
            # can't write (read-only dir, disk full, ...): keep running, warn once
            print(f"저장하지 못했습니다 ({error.__class__.__name__}). 변경 내용은 이번 세션에만 유지됩니다.")

    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
            quizzes = [Quiz.from_dict(d) for d in data.get("quizzes", [])]
            self.history = data.get("history", [])  # forward-tolerant: old files w/o history -> []
            self.source = "file"
            return quizzes
        except FileNotFoundError:
            self.source = "new"
            self.history = []
            return default_quizzes()
        except PermissionError:
            self.source = "denied"
            self.history = []
            return default_quizzes()
        except (json.JSONDecodeError, KeyError, TypeError, AttributeError):
            self._backup_corrupt()        # preserve the bad file before it's overwritten
            self.source = "corrupt"
            self.history = []
            return default_quizzes()
        # FileNotFoundError: no file, state.json, yet (first run, fresh clone)
        # PermissionError: file exists but we can't read it (OS permissions)
        # json.JSONDecodeError: file exists but isn't valid JSON
        # KeyError: a dict is missing a core field
        # TypeError: the shape is wrong
        # AttributeError: valid JSON but wrong shape

    def _backup_corrupt(self):
        """Copy a corrupt state.json to state.json.bak so it can be recovered by hand.

        The next save overwrites state.json with defaults, so without this the
        original (possibly hand-edited) data would be lost. Best-effort: if even
        the copy fails we still fall back to defaults rather than crash.
        """
        try:
            shutil.copy(self.path, self.path + ".bak")
            print(f"손상된 파일을 {self.path}.bak 으로 백업했습니다.")
        except OSError:
            pass
