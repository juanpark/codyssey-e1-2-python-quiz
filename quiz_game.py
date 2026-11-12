"""QuizGame: orchestrates the game — owns the quizzes and runs the menu loop."""
import unicodedata  # stdlib tool
from input_utils import read_int_in_range
from storage import Storage


def display_width(text: str) -> int:
    """Terminal column width: CJK (Wide/Fullwidth) chars count as 2"""
    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in text)


class QuizGame:
    """orchestrates the game, owns the quizzes, runs the menu loop"""

    def __init__(self):
        self.storage = Storage()
        self.quizzes = self.storage.load()
        self.startup_message = self._load_message()
        self.storage.save(self.quizzes)

    def print_menu(self):
        boundary = "=" * 50
        title = "나만의 퀴즈 게임"
        width = len(boundary)

        # Center the title by hand instead of f"{title:^{width}}":
        # f-string centering counts each character as 1 column, but Korean
        # (CJK) glyphs take 2 terminal columns, so ^ would misalign.
        # Measure the true column count with display_width() and split the
        # leftover space evenly. (Final look still depends on the terminal
        # rendering CJK as 2 columns — standards-compliant ones do.)
        pad = width - display_width(title)
        left = pad // 2
        header = " " * left + title + " " * (pad - left)
        print(boundary + '\n' + header + '\n' + boundary)
        if self.startup_message:
            print(self.startup_message)
            print(boundary)
            self.startup_message = None  # consumed --> hidden on every later render!
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 퀴즈 종료")
        print(boundary)
        # print("선택: ", end="")

    def run(self):
        """runs the game"""
        try:
            while True:
                self.print_menu()
                menu = read_int_in_range("선택: ", 1, 5)
                match menu:
                    case 1:
                        print("todo")
                    case 2:
                        print("todo")
                    case 3:
                        print("todo")
                    case 4:
                        print("todo")
                    case 5:
                        print("퀴즈를 종료합니다...")
                        break
        except (KeyboardInterrupt, EOFError):
            print("퀴즈를 종료합니다...")
            return

    def _load_message(self):
        match self.storage.source:
            case "file":
                return f"저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개)"
            case "new":
                return "처음 실행입니다. 기본 문제로 시작합니다."
            case "corrupt":
                return "저장 파일이 손상되어 기본 문제로 시작합니다."


if __name__ == "__main__":
    QuizGame().run()
