import json
import random
from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="BDAV Bingo",
    page_icon="\U0001f3af",
    layout="centered",
    initial_sidebar_state="collapsed",
)

with (Path(__file__).parent / "prompts.json").open(encoding="utf-8") as prompts_file:
    prompt_entries = json.load(prompts_file)["prompts"]

prompts = [entry["english"] for entry in prompt_entries]
prompts_chinese = [entry["chinese"] for entry in prompt_entries]


if len(prompts) != len(prompts_chinese):
    raise ValueError("English and Chinese prompt lists must have the same length")


def new_board() -> list[int]:
    return random.sample(range(len(prompts)), 9)


def initialize_board() -> None:
    if "board" not in st.session_state:
        st.session_state.board = new_board()
    if "selected" not in st.session_state:
        st.session_state.selected = [False] * 9
    if "notes" not in st.session_state:
        st.session_state.notes = [""] * 9
    if "language" not in st.session_state:
        st.session_state.language = "English"


initialize_board()

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Space+Mono:wght@400;700&display=swap');

    :root {
        --ink: #19231f;
        --muted: #68736d;
        --paper: #f6f4ed;
        --mint: #d9f0df;
        --mint-strong: #9ad4ae;
        --coral: #ee806b;
        --line: #d8ddd5;
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 0%, rgba(238, 128, 107, .15), transparent 27rem),
            radial-gradient(circle at 100% 90%, rgba(154, 212, 174, .22), transparent 30rem),
            var(--paper);
        color: var(--ink);
        font-family: 'DM Sans', sans-serif;
    }

    .block-container {
        max-width: 760px;
        padding: 4.5rem 1.25rem 4rem;
    }

    .eyebrow {
        color: var(--coral);
        font-family: 'Space Mono', monospace;
        font-size: .72rem;
        font-weight: 700;
        letter-spacing: .14em;
        text-transform: uppercase;
    }

    h1 {
        color: var(--ink) !important;
        font-size: clamp(2.8rem, 9vw, 5.5rem) !important;
        letter-spacing: -.07em !important;
        line-height: .95 !important;
        margin: .65rem 0 1rem !important;
    }

    .intro {
        color: var(--muted);
        font-size: 1.05rem;
        line-height: 1.55;
        margin-bottom: 2rem;
        max-width: 34rem;
    }

    div[data-testid='stVerticalBlockBorderWrapper'] {
        background: rgba(255, 255, 255, .5);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: .7rem .7rem .35rem;
        transition: border-color .2s ease, transform .2s ease;
    }

    div[data-testid='stVerticalBlockBorderWrapper']:hover {
        border-color: var(--mint-strong);
        transform: translateY(-2px);
    }

    div[data-testid='stVerticalBlockBorderWrapper']:has(button[kind='primary']) {
        background: var(--mint);
        border-color: var(--mint-strong);
    }

    div[data-testid='stVerticalBlockBorderWrapper'] button {
        border: 0;
        color: var(--ink);
        font-size: .95rem;
        font-weight: 700;
        min-height: 4.3rem;
        padding: .25rem .1rem;
        text-align: left;
        white-space: normal;
    }

    div[data-testid='stVerticalBlockBorderWrapper'] button[kind='primary'] {
        background: transparent;
        color: var(--ink);
    }

    div[data-testid='stVerticalBlockBorderWrapper'] input {
        background: rgba(255, 255, 255, .7);
        border-color: transparent;
        color: var(--ink);
        font-size: .82rem;
    }

    div[data-testid='stHorizontalBlock'] {
        gap: .7rem;
    }

    .stButton button[kind='secondary'] {
        border-color: var(--ink);
        border-radius: 999px;
        color: var(--ink);
        font-weight: 700;
    }

    .status {
        color: var(--muted);
        font-family: 'Space Mono', monospace;
        font-size: .72rem;
        margin: 1.25rem 0 .75rem;
        text-transform: uppercase;
    }

    @media (max-width: 600px) {
        .block-container { padding-top: 2.5rem; }
        div[data-testid='stVerticalBlockBorderWrapper'] { padding: .45rem .45rem .2rem; }
        div[data-testid='stVerticalBlockBorderWrapper'] button { font-size: .82rem; min-height: 4.8rem; }
        div[data-testid='stVerticalBlockBorderWrapper'] input { font-size: .76rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="eyebrow">September 2026 BDAV Roundtable</div>', unsafe_allow_html=True)
st.title("BDAV Bingo")
st.markdown(
    '<div class="intro">Find lab members that satisfy all nine squares to win</div>',
    unsafe_allow_html=True,
)

st.radio(
    "Board language",
    options=("English", "中文"),
    key="language",
    horizontal=True,
    label_visibility="collapsed",
)

prompt_list = prompts if st.session_state.language == "English" else prompts_chinese

completed = sum(st.session_state.selected)
st.markdown(f'<div class="status">{completed} of 9 squares checked</div>', unsafe_allow_html=True)

for row in range(3):
    columns = st.columns(3)
    for column_index, column in enumerate(columns):
        index = row * 3 + column_index
        with column:
            with st.container(border=True):
                button_kind = "primary" if st.session_state.selected[index] else "secondary"
                label = ("✓  " if st.session_state.selected[index] else "○  ") + prompt_list[st.session_state.board[index]]
                if st.button(
                    label,
                    key=f"square_{index}",
                    use_container_width=True,
                    type=button_kind,
                ):
                    st.session_state.selected[index] = not st.session_state.selected[index]
                    st.rerun()
                st.text_input(
                    "Note",
                    key=f"note_{index}",
                    label_visibility="collapsed",
                    placeholder="Add a note...",
                    value=st.session_state.notes[index],
                    on_change=lambda cell_index=index: st.session_state.notes.__setitem__(
                        cell_index, st.session_state[f"note_{cell_index}"]
                    ),
                )

st.write("")
if st.button("Shuffle a fresh board", use_container_width=False):
    st.session_state.board = new_board()
    st.session_state.selected = [False] * 9
    st.session_state.notes = [""] * 9
    for index in range(9):
        st.session_state.pop(f"note_{index}", None)
    st.rerun()
