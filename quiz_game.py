"""QuizGame: orchestrates the game — owns the quizzes and runs the menu loop."""
import time
import unicodedata  # stdlib tool
from datetime import datetime
from input_utils import read_int_in_range, read_nonempty
from quiz import Quiz
from storage import Storage


def display_width(text: str) -> int:
    """Terminal column width: CJK (Wide/Fullwidth) chars count as 2"""
    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in text)


class QuizGame:
    """orchestrates the game, owns the quizzes, runs the menu loop"""

    def __init__(self):
        self.storage = Storage()
        self.quizzes = self.storage.load()
        self.history = self.storage.history
        self.startup_message = self._load_message()
        self.storage.save(self.quizzes, self.history)

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
                        self.play()
                    case 2:
                        self.add_quiz()
                    case 3:
                        self.list_quizzes()
                    case 4:
                        self.show_score()
                    case 5:
                        print("퀴즈를 종료합니다...")
                        break
        except (KeyboardInterrupt, EOFError):
            print("\n퀴즈를 종료합니다...")
            return

    def _load_message(self):
        match self.storage.source:
            case "file":
                best = self.best_run()
                if best:
                    return (f"저장된 데이터를 불러왔습니다. "
                            f"(퀴즈 {len(self.quizzes)}개, 최고점수 {self._record_pct(best):.0f}점)")
                return f"저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개)"
            case "new":
                return "처음 실행입니다. 기본 문제로 시작합니다."
            case "corrupt":
                return "저장 파일이 손상되어 기본 문제로 시작합니다."

    @staticmethod
    def _record_pct(record):
        """Percentage score of one history record. total defaults to 1 to avoid /0."""
        return record.get("correct", 0) / record.get("total", 1) * 100

    def best_run(self):
        """The history record with the highest percentage, or None if no games yet."""
        if not self.history:
            return None
        return max(self.history, key=self._record_pct)

    def play(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다. 먼저 '퀴즈 추가'로 문제를 만들어 주세요.")
            return

        total = len(self.quizzes)

        print(f"\n퀴즈를 시작합니다! (총 {total}문제)\n")
        print("=" * 50)

        correct = 0
        for number, quiz in enumerate(self.quizzes, start=1):
            time.sleep(0.5)
            print(f"[문제 {number}]")
            quiz.display()
            print()
            answer = read_int_in_range("정답 입력: ", 1, 4)
            if quiz.is_correct(answer):
                print("정답입니다!")
                print()
                correct += 1
            else:
                print("오답입니다!")
                print()
            print("=" * 50)

        score = correct / total * 100
        print("=" * 50)
        print(f"결과: {total}문제 중 {correct}문제 정답! ({score:.1f}점)")

        # record this game in history, then flag a new best (vs the PRIOR best)
        prior_best = self.best_run()
        self.history.append({
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "correct": correct,
            "total": total,
        })
        if prior_best is None or score > self._record_pct(prior_best):
            print("🎉 최고 점수 갱신!")
        print("=" * 50)
        self.storage.save(self.quizzes, self.history)

    def show_score(self):
        """Show the best run and recent game history (점수 기록)."""
        best = self.best_run()
        if best is None:
            print("아직 플레이 기록이 없습니다. '퀴즈 풀기'로 첫 게임을 시작해 보세요.")
            return
        print(f"\n🏆 최고 점수: {self._record_pct(best):.0f}점 "
              f"({best.get('total', 0)}문제 중 {best.get('correct', 0)}문제 정답)")
        print("=" * 50)
        print("최근 기록:")
        for record in reversed(self.history[-5:]):  # last 5 games, newest first
            print(f"  {record.get('datetime', '?')}  —  "
                  f"{record.get('total', 0)}문제 중 {record.get('correct', 0)}문제 "
                  f"({self._record_pct(record):.0f}점)")
        print("=" * 50)

    def list_quizzes(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다. 먼저 '퀴즈 추가'로 문제를 만들어 주세요.")
            return
        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print("=" * 50)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print("=" * 50)

    def add_quiz(self):
        """Create a new Quiz from user input, append it, and save."""
        print("\n새 퀴즈를 추가합니다.")
        print("=" * 50)
        question = read_nonempty("질문: ")
        choices = [read_nonempty(f"보기 {i}: ") for i in range(1, 5)]
        answer = read_int_in_range("정답 번호 (1-4): ", 1, 4)
        hint = input("힌트 (선택, Enter로 건너뛰기): ").strip() or None
        self.quizzes.append(Quiz(question, choices, answer, hint))
        self.storage.save(self.quizzes, self.history)
        print("=" * 50)
        print(f"추가 완료! (현재 퀴즈 {len(self.quizzes)}개)")


if __name__ == "__main__":
    QuizGame().run()
