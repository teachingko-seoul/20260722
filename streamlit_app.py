import random
from fractions import Fraction

import streamlit as st


# =========================================================
# 1. 웹 페이지 기본 설정
# =========================================================
st.set_page_config(
    page_title="수학 퀴즈",
    page_icon="🧮",
    layout="centered",
)


# =========================================================
# 2. 공통 함수
# =========================================================
def is_prime(number):
    """
    전달받은 숫자가 소수인지 판별하는 함수입니다.

    소수:
    1보다 큰 자연수 중에서
    약수가 1과 자기 자신뿐인 수
    """

    if number < 2:
        return False

    # number의 제곱근까지만 검사하면 됩니다.
    for divisor in range(2, int(number**0.5) + 1):
        if number % divisor == 0:
            return False

    return True


def fraction_to_text(number):
    """
    Fraction 형태의 유리수를 화면에 보기 좋게 표시합니다.

    예:
    Fraction(3, 1)  → 3
    Fraction(2, 5)  → 2/5
    Fraction(-3, 4) → -3/4
    """

    if number.denominator == 1:
        return str(number.numerator)

    return f"{number.numerator}/{number.denominator}"


def make_random_fraction(allow_zero=True):
    """
    임의의 유리수를 만드는 함수입니다.

    분자: -9부터 9
    분모: 1부터 9

    allow_zero=False이면 0이 나오지 않습니다.
    """

    while True:
        numerator = random.randint(-9, 9)
        denominator = random.randint(1, 9)

        if allow_zero or numerator != 0:
            return Fraction(numerator, denominator)


def parse_user_answer(answer_text):
    """
    사용자가 입력한 문자열을 Fraction으로 변환합니다.

    입력 가능 예:
    3
    -2
    1/2
    -3/4
    0.5
    -1.25
    """

    cleaned_answer = answer_text.strip().replace(" ", "")

    if not cleaned_answer:
        raise ValueError("답을 입력하지 않았습니다.")

    try:
        return Fraction(cleaned_answer)
    except (ValueError, ZeroDivisionError):
        raise ValueError(
            "정수, 소수 또는 분수 형태로 입력해 주세요. 예: 3, -2, 0.5, 3/4"
        )


# =========================================================
# 3. 세션 상태 초기화
# =========================================================
# Streamlit은 버튼을 누를 때마다 코드가 처음부터 다시 실행됩니다.
# 따라서 문제와 점수를 session_state에 저장해야 합니다.

if "prime_number" not in st.session_state:
    st.session_state.prime_number = random.randint(1, 100)

if "prime_correct" not in st.session_state:
    st.session_state.prime_correct = 0

if "prime_total" not in st.session_state:
    st.session_state.prime_total = 0


if "sign_numbers" not in st.session_state:
    st.session_state.sign_numbers = [
        make_random_fraction() for _ in range(7)
    ]

if "sign_correct" not in st.session_state:
    st.session_state.sign_correct = 0

if "sign_total" not in st.session_state:
    st.session_state.sign_total = 0


if "calculation_numbers" not in st.session_state:
    st.session_state.calculation_numbers = [
        make_random_fraction(allow_zero=False)
        for _ in range(3)
    ]

if "calculation_operator" not in st.session_state:
    st.session_state.calculation_operator = random.choice(
        ["+", "-", "×", "÷"]
    )

if "calculation_correct" not in st.session_state:
    st.session_state.calculation_correct = 0

if "calculation_total" not in st.session_state:
    st.session_state.calculation_total = 0


# =========================================================
# 4. 문제 생성 함수
# =========================================================
def make_new_prime_question():
    """새로운 소수 판별 문제를 만듭니다."""

    st.session_state.prime_number = random.randint(1, 100)


def make_new_sign_question():
    """새로운 유리수 부호 판별 문제를 만듭니다."""

    st.session_state.sign_numbers = [
        make_random_fraction() for _ in range(7)
    ]


def make_new_calculation_question():
    """새로운 유리수 사칙연산 문제를 만듭니다."""

    operator = random.choice(["+", "-", "×", "÷"])

    # 나눗셈에서는 0으로 나눌 수 없으므로
    # 모든 수가 0이 아니도록 생성합니다.
    if operator == "÷":
        numbers = [
            make_random_fraction(allow_zero=False)
            for _ in range(3)
        ]
    else:
        numbers = [
            make_random_fraction()
            for _ in range(3)
        ]

    st.session_state.calculation_numbers = numbers
    st.session_state.calculation_operator = operator


def calculate_fraction_answer(numbers, operator):
    """
    유리수 3개의 사칙연산 정답을 계산합니다.

    계산은 왼쪽부터 순서대로 진행합니다.

    예:
    1/2 - 1/3 - 1/4
    → (1/2 - 1/3) - 1/4
    """

    first_number, second_number, third_number = numbers

    if operator == "+":
        return first_number + second_number + third_number

    if operator == "-":
        return first_number - second_number - third_number

    if operator == "×":
        return first_number * second_number * third_number

    if operator == "÷":
        return first_number / second_number / third_number

    raise ValueError("지원하지 않는 연산자입니다.")


# =========================================================
# 5. 앱 제목
# =========================================================
st.title("🧮 유리수와 소수 퀴즈")

st.write(
    """
    세 가지 수학 퀴즈를 풀어 보세요.  
    각 탭에서 문제를 확인하고 정답을 선택하거나 입력하면 됩니다.
    """
)

st.divider()


# =========================================================
# 6. 퀴즈 탭 만들기
# =========================================================
prime_tab, sign_tab, calculation_tab = st.tabs(
    [
        "① 소수 판별",
        "② 유리수 부호",
        "③ 유리수 사칙연산",
    ]
)


# =========================================================
# 7. 첫 번째 퀴즈: 소수 판별
# =========================================================
with prime_tab:
    st.header("① 소수 판별 퀴즈")

    st.write("다음 수가 소수인지 판단해 보세요.")

    prime_number = st.session_state.prime_number

    st.markdown(
        f"""
        <div style="
            text-align:center;
            font-size:60px;
            font-weight:bold;
            padding:25px;
            margin:15px 0;
            border:3px solid #4CAF50;
            border-radius:15px;
        ">
            {prime_number}
        </div>
        """,
        unsafe_allow_html=True,
    )

    prime_choice = st.radio(
        "정답을 선택하세요.",
        ["소수입니다.", "소수가 아닙니다."],
        key="prime_choice",
        index=None,
    )

    col1, col2 = st.columns(2)

    with col1:
        check_prime = st.button(
            "정답 확인",
            key="check_prime",
            type="primary",
            use_container_width=True,
        )

    with col2:
        new_prime = st.button(
            "새 문제",
            key="new_prime",
            use_container_width=True,
        )

    if check_prime:
        if prime_choice is None:
            st.warning("먼저 정답을 선택해 주세요.")

        else:
            correct_choice = (
                "소수입니다."
                if is_prime(prime_number)
                else "소수가 아닙니다."
            )

            st.session_state.prime_total += 1

            if prime_choice == correct_choice:
                st.session_state.prime_correct += 1
                st.success("정답입니다.")

            else:
                if prime_number == 1:
                    st.error(
                        "오답입니다. 1은 소수도 아니고 합성수도 아닙니다."
                    )

                elif is_prime(prime_number):
                    st.error(
                        f"오답입니다. {prime_number}은 소수입니다."
                    )

                else:
                    st.error(
                        f"오답입니다. {prime_number}은 소수가 아니고 합성수입니다."
                    )

            # 정답 설명
            if prime_number == 1:
                st.info("1은 약수가 1개이므로 소수도 합성수도 아닙니다.")

            elif is_prime(prime_number):
                st.info(
                    f"{prime_number}의 약수는 1과 "
                    f"{prime_number}뿐입니다."
                )

            else:
                factors = [
                    divisor
                    for divisor in range(2, prime_number)
                    if prime_number % divisor == 0
                ]

                if factors:
                    st.info(
                        f"{prime_number}은 {factors[0]}로 나누어지므로 "
                        "합성수입니다."
                    )

    if new_prime:
        make_new_prime_question()
        st.rerun()

    st.metric(
        "소수 퀴즈 점수",
        f"{st.session_state.prime_correct} / "
        f"{st.session_state.prime_total}",
    )


# =========================================================
# 8. 두 번째 퀴즈: 유리수 7개의 합의 부호
# =========================================================
with sign_tab:
    st.header("② 유리수의 합과 부호 퀴즈")

    st.write(
        "다음 유리수 7개를 모두 더했을 때 결과의 부호를 선택하세요."
    )

    sign_numbers = st.session_state.sign_numbers

    sign_expression = " + ".join(
        f"({fraction_to_text(number)})"
        if number < 0
        else fraction_to_text(number)
        for number in sign_numbers
    )

    st.markdown(
        f"""
        <div style="
            text-align:center;
            font-size:27px;
            font-weight:bold;
            padding:25px;
            margin:15px 0;
            border:3px solid #2196F3;
            border-radius:15px;
            line-height:1.8;
        ">
            {sign_expression}
        </div>
        """,
        unsafe_allow_html=True,
    )

    sign_choice = st.radio(
        "계산 결과의 부호를 선택하세요.",
        ["양수", "0", "음수"],
        key="sign_choice",
        index=None,
        horizontal=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        check_sign = st.button(
            "정답 확인",
            key="check_sign",
            type="primary",
            use_container_width=True,
        )

    with col2:
        new_sign = st.button(
            "새 문제",
            key="new_sign",
            use_container_width=True,
        )

    if check_sign:
        if sign_choice is None:
            st.warning("먼저 양수, 0, 음수 중 하나를 선택해 주세요.")

        else:
            sign_answer = sum(sign_numbers, Fraction(0, 1))

            if sign_answer > 0:
                correct_sign = "양수"

            elif sign_answer < 0:
                correct_sign = "음수"

            else:
                correct_sign = "0"

            st.session_state.sign_total += 1

            if sign_choice == correct_sign:
                st.session_state.sign_correct += 1
                st.success("정답입니다.")

            else:
                st.error("오답입니다.")

            st.info(
                f"계산 결과는 {fraction_to_text(sign_answer)}이고, "
                f"부호는 {correct_sign}입니다."
            )

    if new_sign:
        make_new_sign_question()
        st.rerun()

    st.metric(
        "유리수 부호 퀴즈 점수",
        f"{st.session_state.sign_correct} / "
        f"{st.session_state.sign_total}",
    )


# =========================================================
# 9. 세 번째 퀴즈: 유리수 3개의 사칙연산
# =========================================================
with calculation_tab:
    st.header("③ 유리수 사칙연산 퀴즈")

    st.write(
        "다음 유리수의 계산 결과를 입력하세요. "
        "계산은 왼쪽부터 순서대로 합니다."
    )

    calculation_numbers = st.session_state.calculation_numbers
    calculation_operator = st.session_state.calculation_operator

    number1, number2, number3 = calculation_numbers

    calculation_expression = (
        f"{fraction_to_text(number1)} "
        f"{calculation_operator} "
        f"{fraction_to_text(number2)} "
        f"{calculation_operator} "
        f"{fraction_to_text(number3)}"
    )

    st.markdown(
        f"""
        <div style="
            text-align:center;
            font-size:38px;
            font-weight:bold;
            padding:25px;
            margin:15px 0;
            border:3px solid #FF9800;
            border-radius:15px;
        ">
            {calculation_expression}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "답은 정수, 소수 또는 분수로 입력할 수 있습니다. "
        "예: 3, -2, 0.5, 3/4"
    )

    user_calculation_answer = st.text_input(
        "계산 결과를 입력하세요.",
        key="calculation_input",
        placeholder="예: -3/4",
    )

    col1, col2 = st.columns(2)

    with col1:
        check_calculation = st.button(
            "정답 확인",
            key="check_calculation",
            type="primary",
            use_container_width=True,
        )

    with col2:
        new_calculation = st.button(
            "새 문제",
            key="new_calculation",
            use_container_width=True,
        )

    if check_calculation:
        try:
            user_fraction = parse_user_answer(
                user_calculation_answer
            )

            correct_answer = calculate_fraction_answer(
                calculation_numbers,
                calculation_operator,
            )

            st.session_state.calculation_total += 1

            if user_fraction == correct_answer:
                st.session_state.calculation_correct += 1
                st.success("정답입니다.")

            else:
                st.error("오답입니다.")

            st.info(
                f"정답은 {fraction_to_text(correct_answer)}입니다."
            )

        except ValueError as error:
            st.warning(str(error))

    if new_calculation:
        make_new_calculation_question()

        # 입력 칸을 비워 주기 위해 해당 세션 상태를 삭제합니다.
        if "calculation_input" in st.session_state:
            del st.session_state.calculation_input

        st.rerun()

    st.metric(
        "사칙연산 퀴즈 점수",
        f"{st.session_state.calculation_correct} / "
        f"{st.session_state.calculation_total}",
    )


# =========================================================
# 10. 전체 점수
# =========================================================
st.divider()
st.subheader("📊 전체 학습 결과")

total_correct = (
    st.session_state.prime_correct
    + st.session_state.sign_correct
    + st.session_state.calculation_correct
)

total_questions = (
    st.session_state.prime_total
    + st.session_state.sign_total
    + st.session_state.calculation_total
)

score_col1, score_col2, score_col3 = st.columns(3)

with score_col1:
    st.metric("정답 수", total_correct)

with score_col2:
    st.metric("풀이 수", total_questions)

with score_col3:
    if total_questions == 0:
        accuracy = 0
    else:
        accuracy = round(
            total_correct / total_questions * 100,
            1,
        )

    st.metric("정답률", f"{accuracy}%")