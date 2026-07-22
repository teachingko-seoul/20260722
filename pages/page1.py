import random
import streamlit as st


def is_prime(number):
    """자연수가 소수인지 판별합니다."""

    if number < 2:
        return False

    for divisor in range(2, int(number ** 0.5) + 1):
        if number % divisor == 0:
            return False

    return True


def create_prime_question():
    """새로운 소수 판별 문제를 만듭니다."""

    st.session_state.prime_number = random.randint(1, 100)
    st.session_state.prime_checked = False
    st.session_state.prime_result = None
    st.session_state.prime_question_id += 1


# ---------------------------------------------------------
# Session State 초기화
# ---------------------------------------------------------
if "prime_question_id" not in st.session_state:
    st.session_state.prime_question_id = 0

if "prime_number" not in st.session_state:
    st.session_state.prime_number = random.randint(1, 100)

if "prime_checked" not in st.session_state:
    st.session_state.prime_checked = False

if "prime_result" not in st.session_state:
    st.session_state.prime_result = None


# ---------------------------------------------------------
# 화면 구성
# ---------------------------------------------------------
st.header("① 소수인지 판별하기")

st.info(
    "화면에 제시된 자연수가 소수인지 소수가 아닌지 선택하세요."
)

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
    key=f"prime_choice_{st.session_state.prime_question_id}",
    horizontal=True,
)

column1, column2 = st.columns(2)

with column1:
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

with column2:
    if st.button(
        "새 문제",
        key="new_prime",
        use_container_width=True,
    ):
        create_prime_question()
        st.rerun()


# ---------------------------------------------------------
# 결과 출력
# ---------------------------------------------------------
if st.session_state.prime_checked:
    number = st.session_state.prime_number

    if st.session_state.prime_result == "correct":
        st.success("🎉 정답입니다!")
    else:
        st.error("❌ 오답입니다.")

    if number == 1:
        st.info(
            "1은 소수도 아니고 합성수도 아닙니다."
        )

    elif is_prime(number):
        st.info(
            f"{number}은(는) 1과 {number}만을 약수로 가지므로 "
            "소수입니다."
        )

    else:
        divisor = next(
            value
            for value in range(2, number)
            if number % value == 0
        )

        quotient = number // divisor

        st.info(
            f"{number}은(는) 소수가 아니고 합성수입니다. "
            f"{number} = {divisor} × {quotient}입니다."
        )