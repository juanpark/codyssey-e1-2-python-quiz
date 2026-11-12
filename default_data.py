from quiz import Quiz


def default_quizzes() -> list[Quiz]:
    return [
        Quiz(
            "참(True)과 거짓(False) 두 값만 가지는 파이썬 자료형은?",
            [
                "int",
                "str",
                "bool",
                "list",
            ],
            3,
            "값이 딱 두 개뿐(참 아니면 거짓)."
        ),
        Quiz(
            "리스트 nums = [10, 20, 30, 40] 에서 nums[1] 의 값은?",
            [
                "10",
                "20",
                "30",
                "40",
            ],
            2,
            "파이썬 인덱스는 0부터 센다."
        ),
        Quiz(
            "'python'[1:4] 의 결과는?",
            [
                "'pyt'",
                "'yth'",
                "'ytho'",
                "'pyth'",
            ],
            2,
            "시작 인덱스는 포함, 끝 인덱스는 제외."
        ),
        Quiz(
            "7 // 2 의 결과는?",
            [
                "3.5",
                "3",
                "4",
                "3.0",
            ],
            2,
            "// 는 몫만 남기는 정수 나눗셈(버림)."
        ),
        Quiz("""다음 코드의 출력은?
a = [1, 2, 3]
b = a
b.append(4)
print(len(a))""",
             [
                 "3",
                 "4",
                 "오류 발생",
                 "None",
             ],
             2,
             "b = a 는 복사가 아니라 같은 리스트를 가리킨다(같은 객체)."
             )
    ]


if __name__ == '__main__':
    for q in default_quizzes():
        q.display()
        print()
