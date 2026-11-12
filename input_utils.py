"""helpers for reading validated input from the console."""


def read_int_in_range(prompt: str, low: int, high: int) -> int:
    """Read an integer in [low, high] from the console.

    Re-prompt until the input is a whole number within range; blank,
    non-numeric, and out-of-range entries print a message and retry.
    EOFError/KeyboardInterrupt are not caught here -- they propagate.
    """
    while True:
        raw = input(prompt).strip()

        try:
            value = int(raw)
        except ValueError:
            print(f"{low}~{high} 사이의 숫자를 입력하세요.")
            continue
        if not low <= value <= high:
            print(f"{low}~{high} 사이의 숫자를 입력하세요.")
            continue
        return value


if __name__ == "__main__":
    print(read_int_in_range("Question? ", 1, 4))
