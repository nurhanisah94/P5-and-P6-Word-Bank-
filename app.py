import streamlit as st
import random

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Synonym Quest 🔤",
    page_icon="🔤",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&family=Fredoka+One&display=swap');

  html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
    background-color: #F0F4FF;
  }

  h1 { font-family: 'Fredoka One', cursive; color: #4B3FD8; font-size: 2.6rem; }
  h2, h3 { font-family: 'Fredoka One', cursive; color: #4B3FD8; }

  .base-word-card {
    background: linear-gradient(135deg, #6C63FF, #4B3FD8);
    border-radius: 20px;
    padding: 28px 24px;
    text-align: center;
    color: white;
    margin-bottom: 20px;
    box-shadow: 0 6px 20px rgba(75,63,216,0.35);
  }
  .base-word-card .label {
    font-size: 0.95rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    opacity: 0.85;
    margin-bottom: 6px;
  }
  .base-word-card .word {
    font-family: 'Fredoka One', cursive;
    font-size: 3rem;
    line-height: 1.1;
  }
  .base-word-card .meaning {
    font-size: 1rem;
    opacity: 0.9;
    margin-top: 8px;
  }

  .score-bar {
    display: flex;
    justify-content: center;
    gap: 32px;
    background: white;
    border-radius: 16px;
    padding: 14px 20px;
    margin-bottom: 18px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
  }
  .score-item { text-align: center; }
  .score-item .s-label { font-size: 0.75rem; letter-spacing: 1px; text-transform: uppercase; color: #888; }
  .score-item .s-value { font-family: 'Fredoka One', cursive; font-size: 1.8rem; }
  .score-item.correct .s-value { color: #22C55E; }
  .score-item.streak  .s-value { color: #F59E0B; }
  .score-item.wrong   .s-value { color: #EF4444; }

  .feedback-correct {
    background: #DCFCE7; border-left: 5px solid #22C55E;
    border-radius: 12px; padding: 16px 20px; margin-top: 14px;
    color: #15803D; font-size: 1rem;
  }
  .feedback-wrong {
    background: #FEE2E2; border-left: 5px solid #EF4444;
    border-radius: 12px; padding: 16px 20px; margin-top: 14px;
    color: #B91C1C; font-size: 1rem;
  }
  .feedback-icon { font-size: 1.5rem; margin-right: 8px; }

  .synonym-chips {
    display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px;
  }
  .chip {
    background: #EEF2FF; color: #4B3FD8;
    border-radius: 20px; padding: 4px 14px;
    font-size: 0.9rem; font-weight: 700;
    border: 2px solid #C7D2FE;
  }

  .stTextInput > div > div > input {
    border-radius: 12px !important;
    border: 2px solid #C7D2FE !important;
    font-size: 1.1rem !important;
    padding: 10px 16px !important;
    font-family: 'Nunito', sans-serif !important;
  }
  .stTextInput > div > div > input:focus {
    border-color: #6C63FF !important;
    box-shadow: 0 0 0 3px rgba(108,99,255,0.2) !important;
  }

  .stButton > button {
    border-radius: 12px !important;
    font-family: 'Fredoka One', cursive !important;
    font-size: 1.1rem !important;
    padding: 10px 28px !important;
    background: linear-gradient(135deg, #6C63FF, #4B3FD8) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 4px 14px rgba(75,63,216,0.3) !important;
    transition: transform 0.1s;
  }
  .stButton > button:hover { transform: translateY(-2px); }

  .hint-box {
    background: #FFFBEB; border: 2px dashed #F59E0B;
    border-radius: 12px; padding: 12px 16px;
    font-size: 0.95rem; color: #92400E; margin-top: 10px;
  }

  .progress-label {
    font-size: 0.85rem; color: #6B7280; text-align: right; margin-bottom: 4px;
  }
</style>
""", unsafe_allow_html=True)

# ── Word bank ─────────────────────────────────────────────────────────────────
WORD_BANK = [
    {
        "base": "happy",
        "meaning": "feeling or showing pleasure or joy",
        "synonyms": ["joyful", "cheerful", "pleased", "glad", "delighted", "content", "merry", "elated", "jolly", "blissful"],
        "hint": "Think of words that describe a big smile on someone's face!",
        "example": "She was happy when she got a puppy.",
    },
    {
        "base": "big",
        "meaning": "large in size or amount",
        "synonyms": ["large", "huge", "giant", "enormous", "great", "massive", "vast", "immense", "colossal", "grand"],
        "hint": "Imagine something that takes up a lot of space!",
        "example": "The big elephant stomped through the jungle.",
    },
    {
        "base": "fast",
        "meaning": "moving or happening quickly",
        "synonyms": ["quick", "swift", "rapid", "speedy", "hasty", "brisk", "nimble", "zippy", "fleet", "snappy"],
        "hint": "Think of a cheetah running!",
        "example": "The fast car zoomed past us.",
    },
    {
        "base": "smart",
        "meaning": "having a quick, intelligent mind",
        "synonyms": ["clever", "intelligent", "bright", "wise", "sharp", "brilliant", "gifted", "brainy", "astute", "savvy"],
        "hint": "Think of someone who always knows the right answer!",
        "example": "She is a smart student who loves to read.",
    },
    {
        "base": "scared",
        "meaning": "feeling frightened or afraid",
        "synonyms": ["afraid", "frightened", "terrified", "fearful", "anxious", "nervous", "startled", "petrified", "timid", "uneasy"],
        "hint": "How do you feel watching a spooky movie?",
        "example": "He was scared of the dark room.",
    },
    {
        "base": "tired",
        "meaning": "feeling the need to sleep or rest",
        "synonyms": ["sleepy", "exhausted", "weary", "drowsy", "worn out", "fatigued", "drained", "lethargic", "spent", "beat"],
        "hint": "How do you feel after a long day at school?",
        "example": "She was tired after the long hike.",
    },
    {
        "base": "small",
        "meaning": "little in size or amount",
        "synonyms": ["tiny", "little", "mini", "petite", "compact", "slight", "minute", "miniature", "microscopic", "wee"],
        "hint": "Think of something that fits in the palm of your hand!",
        "example": "The small kitten curled up in a basket.",
    },
    {
        "base": "cold",
        "meaning": "having a low temperature",
        "synonyms": ["cool", "chilly", "freezing", "icy", "frosty", "frigid", "wintry", "brisk", "nippy", "bitter"],
        "hint": "Think of words to describe a snowy day!",
        "example": "Wrap up – it's very cold outside today.",
    },
    {
        "base": "angry",
        "meaning": "feeling or showing strong displeasure",
        "synonyms": ["mad", "furious", "upset", "annoyed", "irritated", "outraged", "cross", "livid", "irate", "enraged"],
        "hint": "Think of how someone looks when they are really not happy!",
        "example": "He was angry when someone broke his toy.",
    },
    {
        "base": "pretty",
        "meaning": "pleasing to look at; attractive",
        "synonyms": ["beautiful", "lovely", "attractive", "gorgeous", "cute", "elegant", "charming", "fair", "stunning", "handsome"],
        "hint": "Words you'd use to describe a rainbow or a flower!",
        "example": "The pretty butterfly landed on a flower.",
    },
]

# ── Session state ─────────────────────────────────────────────────────────────
def init_state():
    if "word_index"    not in st.session_state: st.session_state.word_index    = 0
    if "score"         not in st.session_state: st.session_state.score         = 0
    if "wrong"         not in st.session_state: st.session_state.wrong         = 0
    if "streak"        not in st.session_state: st.session_state.streak        = 0
    if "best_streak"   not in st.session_state: st.session_state.best_streak   = 0
    if "feedback"      not in st.session_state: st.session_state.feedback      = None
    if "show_hint"     not in st.session_state: st.session_state.show_hint     = False
    if "answered"      not in st.session_state: st.session_state.answered      = False
    if "used_words"    not in st.session_state: st.session_state.used_words    = []
    if "order"         not in st.session_state:
        order = list(range(len(WORD_BANK)))
        random.shuffle(order)
        st.session_state.order = order
    if "input_key"     not in st.session_state: st.session_state.input_key     = 0

init_state()

def current_word():
    idx = st.session_state.order[st.session_state.word_index % len(WORD_BANK)]
    return WORD_BANK[idx]

def check_answer(guess: str):
    word = current_word()
    guess_clean = guess.strip().lower()
    if not guess_clean:
        return
    correct = guess_clean in [s.lower() for s in word["synonyms"]]
    if correct:
        st.session_state.score  += 1
        st.session_state.streak += 1
        st.session_state.best_streak = max(st.session_state.streak, st.session_state.best_streak)
        st.session_state.feedback = ("correct", guess_clean, word)
    else:
        st.session_state.wrong  += 1
        st.session_state.streak  = 0
        st.session_state.feedback = ("wrong", guess_clean, word)
    st.session_state.answered = True

def next_question():
    st.session_state.word_index += 1
    st.session_state.feedback    = None
    st.session_state.show_hint   = False
    st.session_state.answered    = False
    st.session_state.input_key  += 1   # clears the text input

def reset_game():
    for key in ["word_index","score","wrong","streak","best_streak",
                "feedback","show_hint","answered","used_words","order","input_key"]:
        if key in st.session_state:
            del st.session_state[key]

# ── Layout ────────────────────────────────────────────────────────────────────
st.markdown("# 🔤 Synonym Quest")
st.markdown("*Can you find words that mean the same thing?*")

# Score bar
total  = st.session_state.score + st.session_state.wrong
accuracy = int(st.session_state.score / total * 100) if total else 0
st.markdown(f"""
<div class="score-bar">
  <div class="score-item correct">
    <div class="s-label">✅ Correct</div>
    <div class="s-value">{st.session_state.score}</div>
  </div>
  <div class="score-item wrong">
    <div class="s-label">❌ Wrong</div>
    <div class="s-value">{st.session_state.wrong}</div>
  </div>
  <div class="score-item streak">
    <div class="s-label">🔥 Streak</div>
    <div class="s-value">{st.session_state.streak}</div>
  </div>
  <div class="score-item">
    <div class="s-label">🎯 Accuracy</div>
    <div class="s-value" style="color:#6C63FF">{accuracy}%</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Progress bar
q_num   = (st.session_state.word_index % len(WORD_BANK)) + 1
progress = q_num / len(WORD_BANK)
st.markdown(f'<div class="progress-label">Question {q_num} of {len(WORD_BANK)}</div>', unsafe_allow_html=True)
st.progress(progress)

# Base word card
word = current_word()
st.markdown(f"""
<div class="base-word-card">
  <div class="label">Find a synonym for</div>
  <div class="word">{word["base"]}</div>
  <div class="meaning">📖 {word["meaning"]}</div>
</div>
""", unsafe_allow_html=True)

# Example sentence
st.markdown(f'💬 **Example:** *"{word["example"]}"*')

# Hint toggle
col_hint, col_space = st.columns([1, 3])
with col_hint:
    if st.button("💡 Show Hint" if not st.session_state.show_hint else "🙈 Hide Hint"):
        st.session_state.show_hint = not st.session_state.show_hint

if st.session_state.show_hint:
    st.markdown(f'<div class="hint-box">💡 <b>Hint:</b> {word["hint"]}</div>', unsafe_allow_html=True)

st.markdown("---")

# Input + submit (disabled after answering)
if not st.session_state.answered:
    user_input = st.text_input(
        "Type a synonym here:",
        placeholder=f"e.g. a word that means '{word['base']}'…",
        key=f"input_{st.session_state.input_key}",
        label_visibility="visible",
    )

    col_submit, col_skip = st.columns([1, 1])
    with col_submit:
        if st.button("✅ Check Answer"):
            if user_input.strip():
                check_answer(user_input)
            else:
                st.warning("Please type a word first!")
    with col_skip:
        if st.button("⏭️ Skip"):
            st.session_state.wrong  += 1
            st.session_state.streak  = 0
            st.session_state.feedback = ("skip", "", word)
            st.session_state.answered = True

# ── Feedback ──────────────────────────────────────────────────────────────────
if st.session_state.feedback:
    kind, guess, w = st.session_state.feedback
    synonyms_display = ", ".join(w["synonyms"][:6])

    if kind == "correct":
        st.markdown(f"""
        <div class="feedback-correct">
          <span class="feedback-icon">🎉</span>
          <b>Brilliant!</b> "<i>{guess}</i>" is a great synonym for "<b>{w['base']}</b>"!<br><br>
          🧠 <b>Why?</b> Both words mean the same thing: <i>{w['meaning']}</i>. Words with the same (or very similar) meaning are called <b>synonyms</b>.
        </div>
        """, unsafe_allow_html=True)
        if st.session_state.streak >= 3:
            st.balloons()

    elif kind == "wrong":
        st.markdown(f"""
        <div class="feedback-wrong">
          <span class="feedback-icon">🤔</span>
          <b>Not quite!</b> "<i>{guess}</i>" doesn't mean the same as "<b>{w['base']}</b>".<br><br>
          🧠 <b>Remember:</b> "{w['base']}" means <i>{w['meaning']}</i>. Here are some real synonyms:<br>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(
            '<div class="synonym-chips">' +
            "".join(f'<span class="chip">{s}</span>' for s in w["synonyms"][:7]) +
            "</div>", unsafe_allow_html=True
        )

    elif kind == "skip":
        st.markdown(f"""
        <div class="feedback-wrong">
          <span class="feedback-icon">⏭️</span>
          <b>Skipped!</b> No worries — here are some synonyms for "<b>{w['base']}</b>":<br>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(
            '<div class="synonym-chips">' +
            "".join(f'<span class="chip">{s}</span>' for s in w["synonyms"][:7]) +
            "</div>", unsafe_allow_html=True
        )

    st.markdown("")
    col_next, col_reset = st.columns([1, 1])
    with col_next:
        if st.button("➡️ Next Word"):
            next_question()
            st.rerun()
    with col_reset:
        if st.button("🔄 Restart Game"):
            reset_game()
            st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#9CA3AF; font-size:0.85rem;'>"
    "🏆 Best streak: <b>{}</b> &nbsp;|&nbsp; Keep going — the more you play, the more words you know!"
    "</p>".format(st.session_state.best_streak),
    unsafe_allow_html=True,
)
