import random
from fractions import Fraction

import matplotlib.pyplot as plt
import streamlit as st


# =========================================================
# 1. 웹 앱 기본 설정
# =========================================================
st.set_page_config(
    page_title="유리수와 소수 수학 퀴즈",
    page_icon="🧮",
    layout="wide",
)

st.title("🧮 소수와 유리수 수학 퀴즈")
st.write(
    """
    세 가지 유형의 수학 문제를 풀어 보세요.

    1. 소수와 합성수 판별
    2. 유리수 7개의 합의 부호 판별
    3. 유리수의 사칙연산
    """
)


# =========================================================
# 2. 공통으로 사용하는 함수
# =========================================================
def is_prime(number):
    """
    전달받은 자연수가 소수인지 판별하는 함수입니다.

    소수:
    1보다 큰 자연수 중에서 약수가 1과 자기 자신뿐인 수
    """
    if number < 2:
        return False

    # number의 제곱근까지만 나누어 보면 됩니다.
    for divisor in range(2, int(number ** 0.5) + 1):
        if number % divisor == 0:
            return False

    return True


def make_random_fraction(
    numerator_min=-9,
    numerator_max=9,
    denominator_min=1,
    denominator_max=9,
    allow_zero=True,
):
    """
    임의의 유리수를 Fraction 형태로 만드는 함수입니다.

    예:
    Fraction(3, 4)  →  3/4
    Fraction(-2, 5) → -2/5
    """
    while True:
        numerator = random.randint(numerator_min, numerator_max)
        denominator = random.randint(denominator_min, denominator_max)

        if not allow_zero and numerator == 0:
            continue

        return Fraction(numerator, denominator)


def fraction_to_string(value):
    """
    Fraction 값을 학생이 보기 좋은 문자열로 바꿉니다.

    예:
    Fraction(3, 4) → "3/4"
    Fraction(5, 1) → "5"
    """
    if value.denominator == 1:
        return str(value.numerator)

    return f"{value.numerator}/{value.denominator}"


def fraction_to_latex(value):
    """
    Fraction 값을 수학 기호로 출력하기 위한 LaTeX 문자열로 바꿉니다.

    예:
    Fraction(3, 4)  → \\frac{3}{4}
    Fraction(-3, 4) → -\\frac{3}{4}
    """
    if value.denominator == 1:
        return str(value.numerator)

    if value.numerator < 0:
        return (
            rf"-\frac{{{abs(value.numerator)}}}"
            rf"{{{value.denominator}}}"
        )

    return (
        rf"\frac{{{value.numerator}}}"
        rf"{{{value.denominator}}}"
    )


def parse_fraction(user_text):
    """
    사용자가 입력한 답을 Fraction으로 변환합니다.

    입력 가능한 예:
    3/4
    -2/5
    2
    0.5
    -1.25
    """
    cleaned_text = user_text.strip().replace(" ", "")

    if cleaned_text == "":
        raise ValueError("답을 입력하지 않았습니다.")

    return Fraction(cleaned_text)


def get_sign(value):
    """
    수의 부호를 '양수', '0', '음수' 중 하나로 반환합니다.
    """
    if value > 0:
        return "양수"
    elif value < 0:
        return "음수"
    else:
        return "0"


# =========================================================
# 3. 첫 번째 퀴즈 관련 함수
# =========================================================
def create_prime_question():
    """
    1부터 100까지의 자연수 중 하나를 임의로 선택합니다.
    """
    st.session_state.prime_number = random.randint(1, 100)
    st.session_state.prime_checked = False
    st.session_state.prime_result = None

    # 새 문제를 만들 때 선택값도 초기화합니다.
    st.session_state.prime_choice = "선택하세요"


# =========================================================
# 4. 두 번째 퀴즈 관련 함수
# =========================================================
def create_sign_question():
    """
    유리수 7개를 임의로 생성합니다.

    합이 항상 특정 부호로만 나오지 않도록
    마지막 수를 조절하여 양수, 0, 음수 문제를
    비교적 고르게 생성합니다.
    """
    target_sign = random.choice(["양수", "0", "음수"])

    # 먼저 유리수 6개를 생성합니다.
    numbers = [
        make_random_fraction(
            numerator_min=-6,
            numerator_max=6,
            denominator_min=1,
            denominator_max=6,
        )
        for _ in range(6)
    ]

    first_six_sum = sum(numbers, Fraction(0, 1))

    if target_sign == "0":
        # 전체 합이 0이 되도록 마지막 수를 결정합니다.
        last_number = -first_six_sum

    elif target_sign == "양수":
        # 전체 합이 양수가 되도록 양의 값을 추가합니다.
        positive_amount = make_random_fraction(
            numerator_min=1,
            numerator_max=5,
            denominator_min=1,
            denominator_max=5,
            allow_zero=False,
        )
        last_number = -first_six_sum + positive_amount

    else:
        # 전체 합이 음수가 되도록 음의 값을 추가합니다.
        positive_amount = make_random_fraction(
            numerator_min=1,
            numerator_max=5,
            denominator_min=1,
            denominator_max=5,
            allow_zero=False,
        )
        last_number = -first_six_sum - positive_amount

    numbers.append(last_number)

    # 문제를 섞어서 마지막 수가 조절된 수라는 사실이
    # 보이지 않도록 합니다.
    random.shuffle(numbers)

    st.session_state.sign_numbers = numbers
    st.session_state.sign_sum = sum(numbers, Fraction(0, 1))
    st.session_state.sign_checked = False
    st.session_state.sign_result = None
    st.session_state.sign_choice = "선택하세요"


def draw_number_line(numbers, total):
    """
    유리수 7개와 합을 수직선 위에 표시합니다.
    """
    number_values = [float(number) for number in numbers]
    total_value = float(total)

    all_values = number_values + [total_value, 0]

    minimum_value = min(all_values)
    maximum_value = max(all_values)

    # 그래프 양쪽에 여유 공간을 줍니다.
    value_range = maximum_value - minimum_value

    if value_range == 0:
        margin = 1
    else:
        margin = max(0.7, value_range * 0.15)

    left_limit = minimum_value - margin
    right_limit = maximum_value + margin

    fig, ax = plt.subplots(figsize=(12, 4))

    # 수직선
    ax.axhline(
        y=0,
        linewidth=2,
    )

    # 0의 위치를 강조합니다.
    ax.axvline(
        x=0,
        linestyle="--",
        linewidth=1.5,
        alpha=0.7,
    )

    # 유리수 7개 표시
    for index, number in enumerate(numbers):
        x_value = float(number)

        # 글자가 겹치는 것을 줄이기 위해 위아래로 번갈아 표시합니다.
        if index % 2 == 0:
            text_y = 0.23
        else:
            text_y = -0.28

        ax.scatter(
            x_value,
            0,
            s=80,
            zorder=3,
        )

        ax.text(
            x_value,
            text_y,
            f"{index + 1}번\n{fraction_to_string(number)}",
            ha="center",
            va="center",
            fontsize=10,
        )

    # 합 표시
    ax.scatter(
        total_value,
        0,
        s=220,
        marker="*",
        zorder=5,
    )

    ax.text(
        total_value,
        0.55,
        f"합 = {fraction_to_string(total)}",
        ha="center",
        va="center",
        fontsize=13,
        fontweight="bold",
    )

    ax.set_xlim(left_limit, right_limit)
    ax.set_ylim(-0.7, 0.9)

    ax.set_yticks([])
    ax.set_xlabel("수직선")
    ax.set_title("유리수 7개와 합의 위치")

    # 위쪽, 왼쪽, 오른쪽 테두리를 제거합니다.
    ax.spines["top"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.grid(
        axis="x",
        linestyle=":",
        alpha=0.4,
    )

    plt.tight_layout()

    return fig


# =========================================================
# 5. 세 번째 퀴즈 관련 함수
# =========================================================
def create_operation_question():
    """
    유리수 3개와 연산자를 임의로 생성합니다.

    가능한 연산:
    덧셈, 뺄셈, 곱셈, 나눗셈
    """
    operation = random.choice(["덧셈", "뺄셈", "곱셈", "나눗셈"])

    first_number = make_random_fraction(
        numerator_min=-9,
        numerator_max=9,
        denominator_min=1,
        denominator_max=9,
    )

    second_number = make_random_fraction(
        numerator_min=-9,
        numerator_max=9,
        denominator_min=1,
        denominator_max=9,
    )

    # 나눗셈의 경우 나누는 수가 0이 되면 안 됩니다.
    if operation == "나눗셈":
        third_number = make_random_fraction(
            numerator_min=-9,
            numerator_max=9,
            denominator_min=1,
            denominator_max=9,
            allow_zero=False,
        )
    else:
        third_number = make_random_fraction(
            numerator_min=-9,
            numerator_max=9,
            denominator_min=1,
            denominator_max=9,
        )

    if operation == "덧셈":
        answer = first_number + second_number + third_number
        symbol = "+"

    elif operation == "뺄셈":
        answer = first_number - second_number - third_number
        symbol = "-"

    elif operation == "곱셈":
        answer = first_number * second_number * third_number
        symbol = r"\times"

    else:
        # 왼쪽부터 차례대로 계산합니다.
        # (첫 번째 수 ÷ 두 번째 수) ÷ 세 번째 수
        #
        # 두 번째 수도 0이면 안 되므로 다시 생성합니다.
        while second_number == 0:
            second_number = make_random_fraction(
                numerator_min=-9,
                numerator_max=9,
                denominator_min=1,
                denominator_max=9,
                allow_zero=False,
            )

        answer = first_number / second_number / third_number
        symbol = r"\div"

    st.session_state.operation_type = operation
    st.session_state.operation_numbers = [
        first_number,
        second_number,
        third_number,
    ]
    st.session_state.operation_symbol = symbol
    st.session_state.operation_answer = answer
    st.session_state.operation_checked = False
    st.session_state.operation_result = None

    # 문제 번호를 증가시켜 입력창을 새롭게 만듭니다.
    st.session_state.operation_question_id += 1


# =========================================================
# 6. Session State 초기 설정
# =========================================================
if "operation_question_id" not in st.session_state:
    st.session_state.operation_question_id = 0

if "prime_number" not in st.session_state:
    create_prime_question()

if "sign_numbers" not in st.session_state:
    create_sign_question()

if "operation_numbers" not in st.session_state:
    create_operation_question()


# =========================================================
# 7. 탭 만들기
# =========================================================
prime_tab, sign_tab, operation_tab = st.tabs(
    [
        "① 소수 판별",
        "② 유리수의 부호",
        "③ 유리수의 사칙연산",
    ]
)


# =========================================================
# 8. 첫 번째 탭: 소수 판별 퀴즈
# =========================================================
with prime_tab:
    st.header("① 소수인지 판별하기")

    st.info(
        "화면에 제시된 자연수가 소수인지 소수가 아닌지 선택하세요."
    )

    st.subheader("문제")

    st.markdown(
        f"""
        <div style="
            text-align:center;
            font-size:70px;
            font-weight:bold;
            padding:25px;
            border:3px solid #4A90E2;
            border-radius:15px;
            margin:15px 0;
        ">
            {st.session_state.prime_number}
        </div>
        """,
        unsafe_allow_html=True,
    )

    prime_choice = st.radio(
        "이 수를 판별하세요.",
        ["선택하세요", "소수입니다", "소수가 아닙니다"],
        key="prime_choice",
        horizontal=True,
    )

    prime_column1, prime_column2 = st.columns(2)

    with prime_column1:
        if st.button(
            "정답 확인",
            key="check_prime",
            type="primary",
            use_container_width=True,
        ):
            if prime_choice == "선택하세요":
                st.warning("먼저 답을 선택하세요.")

            else:
                number = st.session_state.prime_number
                correct_is_prime = is_prime(number)
                user_says_prime = prime_choice == "소수입니다"

                st.session_state.prime_checked = True

                if user_says_prime == correct_is_prime:
                    st.session_state.prime_result = "correct"
                else:
                    st.session_state.prime_result = "wrong"

    with prime_column2:
        if st.button(
            "새 문제",
            key="new_prime",
            use_container_width=True,
        ):
            create_prime_question()
            st.rerun()

    if st.session_state.prime_checked:
        number = st.session_state.prime_number

        if st.session_state.prime_result == "correct":
            st.success("🎉 정답입니다!")

        else:
            st.error("❌ 오답입니다.")

        # 1은 소수도 아니고 합성수도 아닙니다.
        if number == 1:
            st.info(
                "1은 소수가 아니며, 합성수도 아닙니다. "
                "합성수는 1보다 큰 자연수 중 소수가 아닌 수입니다."
            )

        elif is_prime(number):
            st.info(
                f"{number}은(는) 1과 {number}만을 약수로 가지므로 "
                "소수입니다."
            )

        else:
            divisors = [
                divisor
                for divisor in range(2, number)
                if number % divisor == 0
            ]

            example_divisor = divisors[0]
            quotient = number // example_divisor

            st.info(
                f"{number}은(는) 소수가 아니고 합성수입니다. "
                f"{number} = {example_divisor} × {quotient}로 "
                "나타낼 수 있습니다."
            )


# =========================================================
# 9. 두 번째 탭: 유리수 7개의 합의 부호
# =========================================================
with sign_tab:
    st.header("② 유리수 7개의 합의 부호 판단하기")

    st.info(
        "제시된 유리수 7개를 모두 더한 결과가 "
        "양수, 0, 음수 중 무엇인지 선택하세요."
    )

    numbers = st.session_state.sign_numbers
    total = st.session_state.sign_sum

    numbers_latex = " + ".join(
        [
            rf"\left({fraction_to_latex(number)}\right)"
            for number in numbers
        ]
    )

    st.subheader("문제")
    st.latex(numbers_latex)

    st.write("위 유리수 7개의 합은 어떤 수입니까?")

    sign_choice = st.radio(
        "합의 부호를 선택하세요.",
        ["선택하세요", "양수", "0", "음수"],
        key="sign_choice",
        horizontal=True,
    )

    sign_column1, sign_column2 = st.columns(2)

    with sign_column1:
        if st.button(
            "정답 확인",
            key="check_sign",
            type="primary",
            use_container_width=True,
        ):
            if sign_choice == "선택하세요":
                st.warning("먼저 답을 선택하세요.")

            else:
                correct_sign = get_sign(total)
                st.session_state.sign_checked = True

                if sign_choice == correct_sign:
                    st.session_state.sign_result = "correct"
                else:
                    st.session_state.sign_result = "wrong"

    with sign_column2:
        if st.button(
            "새 문제",
            key="new_sign",
            use_container_width=True,
        ):
            create_sign_question()
            st.rerun()

    if st.session_state.sign_checked:
        correct_sign = get_sign(total)

        if st.session_state.sign_result == "correct":
            st.success("🎉 정답입니다!")

        else:
            st.error("❌ 오답입니다.")

        st.subheader("정답과 풀이")

        st.latex(
            numbers_latex
            + " = "
            + fraction_to_latex(total)
        )

        st.write(
            f"따라서 합은 **{fraction_to_string(total)}**이고, "
            f"정답은 **{correct_sign}**입니다."
        )

        st.subheader("수직선으로 확인하기")

        figure = draw_number_line(numbers, total)
        st.pyplot(figure)
        plt.close(figure)

        st.caption(
            "●은 각각의 유리수이고, ★은 유리수 7개의 합입니다. "
            "점선은 0의 위치를 나타냅니다."
        )


# =========================================================
# 10. 세 번째 탭: 유리수의 사칙연산
# =========================================================
with operation_tab:
    st.header("③ 유리수의 사칙연산")

    st.info(
        "유리수 3개의 계산 결과를 기약분수 또는 소수로 입력하세요. "
        "나눗셈과 뺄셈은 왼쪽부터 차례대로 계산합니다."
    )

    first_number, second_number, third_number = (
        st.session_state.operation_numbers
    )

    symbol = st.session_state.operation_symbol
    operation_type = st.session_state.operation_type

    st.subheader(f"문제: 유리수의 {operation_type}")

    if operation_type in ["뺄셈", "나눗셈"]:
        question_latex = (
            rf"\left("
            rf"{fraction_to_latex(first_number)}"
            rf"\;{symbol}\;"
            rf"{fraction_to_latex(second_number)}"
            rf"\right)"
            rf"\;{symbol}\;"
            rf"{fraction_to_latex(third_number)}"
        )
    else:
        question_latex = (
            rf"{fraction_to_latex(first_number)}"
            rf"\;{symbol}\;"
            rf"{fraction_to_latex(second_number)}"
            rf"\;{symbol}\;"
            rf"{fraction_to_latex(third_number)}"
        )

    st.latex(question_latex + " = \; ?")

    st.write(
        "답은 `3/4`, `-2/5`, `2`, `0.5`와 같은 형태로 입력할 수 있습니다."
    )

    answer_key = (
        f"operation_user_answer_"
        f"{st.session_state.operation_question_id}"
    )

    user_answer_text = st.text_input(
        "답을 입력하세요.",
        placeholder="예: -3/4",
        key=answer_key,
    )

    operation_column1, operation_column2 = st.columns(2)

    with operation_column1:
        if st.button(
            "정답 확인",
            key="check_operation",
            type="primary",
            use_container_width=True,
        ):
            if user_answer_text.strip() == "":
                st.warning("먼저 답을 입력하세요.")

            else:
                try:
                    user_answer = parse_fraction(user_answer_text)
                    correct_answer = (
                        st.session_state.operation_answer
                    )

                    st.session_state.operation_checked = True

                    if user_answer == correct_answer:
                        st.session_state.operation_result = "correct"
                    else:
                        st.session_state.operation_result = "wrong"

                except (ValueError, ZeroDivisionError):
                    st.session_state.operation_checked = False
                    st.error(
                        "답의 형식을 확인하세요. "
                        "예를 들어 3/4, -2, 0.5처럼 입력해야 합니다."
                    )

    with operation_column2:
        if st.button(
            "새 문제",
            key="new_operation",
            use_container_width=True,
        ):
            create_operation_question()
            st.rerun()

    if st.session_state.operation_checked:
        correct_answer = st.session_state.operation_answer

        if st.session_state.operation_result == "correct":
            st.success("🎉 정답입니다!")

        else:
            st.error("❌ 오답입니다.")

        st.subheader("정답")

        st.latex(
            question_latex
            + " = "
            + fraction_to_latex(correct_answer)
        )

        st.write(
            f"정답은 **{fraction_to_string(correct_answer)}**입니다."
        )

        # 소수 값도 함께 보여 줍니다.
        decimal_answer = float(correct_answer)

        st.write(
            f"소수로 나타내면 약 **{decimal_answer:.4f}**입니다."
        )


# =========================================================
# 11. 화면 아래쪽 안내
# =========================================================
st.divider()

st.caption(
    "각 탭의 '새 문제' 버튼을 누르면 새로운 문제가 출제됩니다."
)