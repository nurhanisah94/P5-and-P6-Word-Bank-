import streamlit as st
import random

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Synonym Quest 🔤", page_icon="🔤", layout="centered")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&family=Fredoka+One&display=swap');

  html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
    background-color: #F0F4FF;
  }
  h1 { font-family: 'Fredoka One', cursive; color: #4B3FD8; font-size: 2.6rem; }
  h2, h3 { font-family: 'Fredoka One', cursive; color: #4B3FD8; }

  /* ── Word card ── */
  .base-word-card {
    background: linear-gradient(135deg, #6C63FF, #4B3FD8);
    border-radius: 20px; padding: 28px 24px; text-align: center;
    color: white; margin-bottom: 16px;
    box-shadow: 0 6px 20px rgba(75,63,216,0.35);
  }
  .base-word-card .label {
    font-size:.9rem; letter-spacing:2px; text-transform:uppercase; opacity:.85; margin-bottom:6px;
  }
  .base-word-card .word { font-family:'Fredoka One',cursive; font-size:3rem; line-height:1.1; }
  .base-word-card .meaning { font-size:1rem; opacity:.9; margin-top:8px; }

  /* ── Score bar ── */
  .score-bar {
    display:flex; justify-content:center; gap:28px;
    background:white; border-radius:16px; padding:14px 20px; margin-bottom:16px;
    box-shadow:0 2px 12px rgba(0,0,0,0.07);
  }
  .score-item { text-align:center; }
  .score-item .s-label { font-size:.72rem; letter-spacing:1px; text-transform:uppercase; color:#888; }
  .score-item .s-value { font-family:'Fredoka One',cursive; font-size:1.8rem; }
  .score-item.found   .s-value { color:#22C55E; }
  .score-item.total   .s-value { color:#6C63FF; }
  .score-item.wrong   .s-value { color:#EF4444; }
  .score-item.streak  .s-value { color:#F59E0B; }

  /* ── Found-words chips ── */
  .chips-area { display:flex; flex-wrap:wrap; gap:8px; margin:10px 0 14px; min-height:36px; }
  .chip-found {
    background:#DCFCE7; color:#15803D;
    border-radius:20px; padding:5px 16px;
    font-size:.95rem; font-weight:700; border:2px solid #86EFAC;
    animation: pop .2s ease;
  }
  .chip-all {
    background:#EEF2FF; color:#4B3FD8;
    border-radius:20px; padding:5px 14px;
    font-size:.9rem; font-weight:700; border:2px solid #C7D2FE;
  }
  .chip-missed {
    background:#FEF9C3; color:#854D0E;
    border-radius:20px; padding:5px 14px;
    font-size:.9rem; font-weight:700; border:2px solid #FDE047;
  }
  @keyframes pop { 0%{transform:scale(.7);opacity:0} 100%{transform:scale(1);opacity:1} }

  /* ── Feedback banners ── */
  .fb-correct {
    background:#DCFCE7; border-left:5px solid #22C55E;
    border-radius:12px; padding:12px 18px; margin:8px 0; color:#15803D; font-size:1rem;
  }
  .fb-wrong {
    background:#FEE2E2; border-left:5px solid #EF4444;
    border-radius:12px; padding:12px 18px; margin:8px 0; color:#B91C1C; font-size:1rem;
  }
  .fb-dup {
    background:#FEF3C7; border-left:5px solid #F59E0B;
    border-radius:12px; padding:12px 18px; margin:8px 0; color:#92400E; font-size:1rem;
  }
  .fb-done {
    background:#EDE9FE; border-left:5px solid #8B5CF6;
    border-radius:12px; padding:14px 20px; margin:10px 0; color:#4C1D95; font-size:1rem;
  }

  /* ── Summary card ── */
  .summary-card {
    background:white; border-radius:20px; padding:24px 28px;
    box-shadow:0 4px 18px rgba(0,0,0,0.10); margin-top:16px;
  }

  /* ── Progress ── */
  .progress-label { font-size:.85rem; color:#6B7280; text-align:right; margin-bottom:4px; }

  /* ── Hint ── */
  .hint-box {
    background:#FFFBEB; border:2px dashed #F59E0B;
    border-radius:12px; padding:12px 16px; font-size:.95rem; color:#92400E; margin-top:8px;
  }

  /* ── Buttons ── */
  .stButton > button {
    border-radius:12px !important; font-family:'Fredoka One',cursive !important;
    font-size:1.05rem !important; padding:10px 26px !important;
    background:linear-gradient(135deg,#6C63FF,#4B3FD8) !important;
    color:white !important; border:none !important;
    box-shadow:0 4px 14px rgba(75,63,216,0.28) !important;
  }
  .stButton > button:hover { opacity:.92; }

  /* ── Input ── */
  .stTextInput > div > div > input {
    border-radius:12px !important; border:2px solid #C7D2FE !important;
    font-size:1.1rem !important; padding:10px 16px !important;
    font-family:'Nunito',sans-serif !important;
  }
  .stTextInput > div > div > input:focus {
    border-color:#6C63FF !important;
    box-shadow:0 0 0 3px rgba(108,99,255,.2) !important;
  }
</style>
""", unsafe_allow_html=True)

# ── Word bank ─────────────────────────────────────────────────────────────────
WORD_BANK = [
    {
        "base": "happy",
        "meaning": "feeling or showing pleasure or joy",
        "synonyms": ["joyful","cheerful","pleased","glad","delighted","content","merry","elated","jolly","blissful","gleeful","thrilled","overjoyed","ecstatic","jubilant"],
        "hint": "Think of words that describe a big smile on someone's face!",
        "example": "She was happy when she got a puppy.",
    },
    {
        "base": "big",
        "meaning": "large in size or amount",
        "synonyms": ["large","huge","giant","enormous","great","massive","vast","immense","colossal","grand","bulky","hefty","towering","whopping","gigantic"],
        "hint": "Imagine something that takes up a LOT of space!",
        "example": "The big elephant stomped through the jungle.",
    },
    {
        "base": "fast",
        "meaning": "moving or happening quickly",
        "synonyms": ["quick","swift","rapid","speedy","hasty","brisk","nimble","zippy","fleet","snappy","prompt","hurried","lightning","agile","express"],
        "hint": "Think of a cheetah running at full speed!",
        "example": "The fast car zoomed past us.",
    },
    {
        "base": "smart",
        "meaning": "having a quick, intelligent mind",
        "synonyms": ["clever","intelligent","bright","wise","sharp","brilliant","gifted","brainy","astute","savvy","shrewd","quick-witted","knowledgeable","genius","perceptive"],
        "hint": "Think of someone who always knows the right answer!",
        "example": "She is a smart student who loves to read.",
    },
    {
        "base": "scared",
        "meaning": "feeling frightened or afraid",
        "synonyms": ["afraid","frightened","terrified","fearful","anxious","nervous","startled","petrified","timid","uneasy","spooked","panicked","shaky","horrified","alarmed"],
        "hint": "How do you feel watching a spooky movie?",
        "example": "He was scared of the dark room.",
    },
    {
        "base": "tired",
        "meaning": "feeling the need to sleep or rest",
        "synonyms": ["sleepy","exhausted","weary","drowsy","worn out","fatigued","drained","lethargic","spent","beat","groggy","sluggish","burnt out","listless","languid"],
        "hint": "How do you feel after a really long day at school?",
        "example": "She was tired after the long hike.",
    },
    {
        "base": "small",
        "meaning": "little in size or amount",
        "synonyms": ["tiny","little","mini","petite","compact","slight","minute","miniature","microscopic","wee","puny","dainty","teeny","itsy-bitsy","dinky"],
        "hint": "Think of something that fits in the palm of your hand!",
        "example": "The small kitten curled up in a basket.",
    },
    {
        "base": "cold",
        "meaning": "having a low temperature",
        "synonyms": ["cool","chilly","freezing","icy","frosty","frigid","wintry","brisk","nippy","bitter","arctic","glacial","crisp","raw","biting"],
        "hint": "Think of words to describe a snowy winter day!",
        "example": "Wrap up — it's very cold outside today.",
    },
    {
        "base": "angry",
        "meaning": "feeling or showing strong displeasure",
        "synonyms": ["mad","furious","upset","annoyed","irritated","outraged","cross","livid","irate","enraged","fuming","seething","bitter","hostile","displeased"],
        "hint": "Think of how someone looks when they are really not happy!",
        "example": "He was angry when someone broke his toy.",
    },
    {
        "base": "pretty",
        "meaning": "pleasing to look at; attractive",
        "synonyms": ["beautiful","lovely","attractive","gorgeous","cute","elegant","charming","fair","stunning","handsome","radiant","graceful","dazzling","exquisite","alluring"],
        "hint": "Words you'd use to describe a rainbow or a flower!",
        "example": "The pretty butterfly landed on a flower.",
    },
]

# ── Session state ─────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "word_index":   0,
        "total_score":  0,       # cumulative points across all words
        "total_wrong":  0,       # cumulative wrong guesses
        "found":        [],      # synonyms found for current word
        "wrong_this":   0,       # wrong guesses for current word
        "last_fb":      None,    # ("correct"|"wrong"|"dup", word_string)
        "done_word":    False,   # player finished this word (moved on)
        "show_hint":    False,
        "input_key":    0,
        "game_over":    False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
    if "order" not in st.session_state:
        order = list(range(len(WORD_BANK)))
        random.shuffle(order)
        st.session_state.order = order

def reset_game():
    for k in ["word_index","total_score","total_wrong","found","wrong_this",
              "last_fb","done_word","show_hint","input_key","game_over","order"]:
        if k in st.session_state:
            del st.session_state[k]

init_state()

def current_word():
    idx = st.session_state.order[st.session_state.word_index % len(WORD_BANK)]
    return WORD_BANK[idx]

def submit_guess(guess: str):
    word = current_word()
    g = guess.strip().lower()
    if not g:
        return
    found_lower = [f.lower() for f in st.session_state.found]
    synonyms_lower = [s.lower() for s in word["synonyms"]]

    if g in found_lower:
        st.session_state.last_fb = ("dup", g)
    elif g in synonyms_lower:
        st.session_state.found.append(g)
        st.session_state.total_score += 1
        st.session_state.last_fb = ("correct", g)
        # Auto-complete if all synonyms found
        if len(st.session_state.found) == len(word["synonyms"]):
            st.session_state.done_word = True
            st.session_state.last_fb = ("all_found", g)
    else:
        st.session_state.wrong_this  += 1
        st.session_state.total_wrong += 1
        st.session_state.last_fb = ("wrong", g)
    st.session_state.input_key += 1

def move_next():
    st.session_state.word_index  += 1
    st.session_state.found        = []
    st.session_state.wrong_this   = 0
    st.session_state.last_fb      = None
    st.session_state.done_word    = False
    st.session_state.show_hint    = False
    st.session_state.input_key   += 1
    if st.session_state.word_index >= len(WORD_BANK):
        st.session_state.game_over = True

# ── GAME OVER screen ──────────────────────────────────────────────────────────
if st.session_state.game_over:
    st.markdown("# 🏆 Game Over!")
    total_possible = sum(len(w["synonyms"]) for w in WORD_BANK)
    pct = int(st.session_state.total_score / total_possible * 100)
    if pct >= 80:
        badge, msg = "🥇", "Outstanding! You're a synonym superstar!"
    elif pct >= 50:
        badge, msg = "🥈", "Great job! You know loads of synonyms!"
    else:
        badge, msg = "🥉", "Good try! Keep practising — you'll get even better!"

    st.markdown(f"""
    <div class="summary-card" style="text-align:center">
      <div style="font-size:4rem">{badge}</div>
      <div style="font-family:'Fredoka One',cursive;font-size:1.6rem;color:#4B3FD8;margin:8px 0">{msg}</div>
      <div style="font-size:1rem;color:#555;margin-top:12px">
        You found <b style="color:#22C55E">{st.session_state.total_score}</b> out of
        <b>{total_possible}</b> possible synonyms ({pct}%).<br>
        Wrong guesses: <b style="color:#EF4444">{st.session_state.total_wrong}</b>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("🔄 Play Again"):
        reset_game()
        st.rerun()
    st.stop()

# ── MAIN GAME ─────────────────────────────────────────────────────────────────
st.markdown("# 🔤 Synonym Quest")
st.markdown("*How many words with the same meaning can YOU think of?*")

word = current_word()
found_count = len(st.session_state.found)
total_count = len(word["synonyms"])

# Score bar
st.markdown(f"""
<div class="score-bar">
  <div class="score-item found">
    <div class="s-label">✅ Found</div>
    <div class="s-value">{found_count}/{total_count}</div>
  </div>
  <div class="score-item total">
    <div class="s-label">⭐ Points</div>
    <div class="s-value">{st.session_state.total_score}</div>
  </div>
  <div class="score-item wrong">
    <div class="s-label">❌ Wrong</div>
    <div class="s-value">{st.session_state.wrong_this}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Progress
q_num = st.session_state.word_index + 1
st.markdown(f'<div class="progress-label">Word {q_num} of {len(WORD_BANK)}</div>', unsafe_allow_html=True)
st.progress(q_num / len(WORD_BANK))

# Word card
st.markdown(f"""
<div class="base-word-card">
  <div class="label">Find as many synonyms as you can for</div>
  <div class="word">{word["base"]}</div>
  <div class="meaning">📖 {word["meaning"]}</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f'💬 **Example:** *"{word["example"]}"*')

# Hint
col_hint, _ = st.columns([1, 3])
with col_hint:
    label = "🙈 Hide Hint" if st.session_state.show_hint else "💡 Show Hint"
    if st.button(label):
        st.session_state.show_hint = not st.session_state.show_hint
if st.session_state.show_hint:
    st.markdown(f'<div class="hint-box">💡 <b>Hint:</b> {word["hint"]}</div>', unsafe_allow_html=True)

st.markdown("---")

# ── Found words display ───────────────────────────────────────────────────────
if st.session_state.found:
    chips_html = "".join(f'<span class="chip-found">✔ {w}</span>' for w in st.session_state.found)
    st.markdown(f'**Words you\'ve found so far ({found_count}):**')
    st.markdown(f'<div class="chips-area">{chips_html}</div>', unsafe_allow_html=True)
else:
    st.markdown("*No synonyms found yet — start typing below!*")

# ── Input area (hidden once player moves on) ──────────────────────────────────
if not st.session_state.done_word:
    user_input = st.text_input(
        "Type a synonym and press **Check**:",
        placeholder=f"Think of another word for '{word['base']}'…",
        key=f"inp_{st.session_state.input_key}",
    )

    col_check, col_done = st.columns([1, 1])
    with col_check:
        if st.button("✅ Check"):
            if user_input.strip():
                submit_guess(user_input)
                st.rerun()
            else:
                st.warning("Please type a word first!")
    with col_done:
        if st.button("➡️ I'm done with this word"):
            st.session_state.done_word = True
            st.session_state.last_fb   = ("reveal", None)
            st.rerun()

# ── Inline feedback ───────────────────────────────────────────────────────────
fb = st.session_state.last_fb
if fb and not st.session_state.done_word:
    kind = fb[0]; g = fb[1] if len(fb) > 1 else ""
    if kind == "correct":
        st.markdown(f'<div class="fb-correct">🎉 <b>Yes!</b> "<i>{g}</i>" is a synonym for <b>{word["base"]}</b>! +1 point</div>', unsafe_allow_html=True)
    elif kind == "wrong":
        st.markdown(f'<div class="fb-wrong">🤔 "<i>{g}</i>" doesn\'t quite mean the same as <b>{word["base"]}</b>. Try again!</div>', unsafe_allow_html=True)
    elif kind == "dup":
        st.markdown(f'<div class="fb-dup">👀 You already found "<i>{g}</i>"! Try a different word.</div>', unsafe_allow_html=True)
    elif kind == "all_found":
        st.markdown(f'<div class="fb-done">🏆 <b>Amazing!</b> You found ALL {total_count} synonyms for <b>{word["base"]}</b>!</div>', unsafe_allow_html=True)
        st.balloons()

# ── Reveal + Next (shown after player is done) ────────────────────────────────
if st.session_state.done_word:
    missed = [s for s in word["synonyms"] if s.lower() not in [f.lower() for f in st.session_state.found]]

    if found_count == total_count:
        st.markdown(f'<div class="fb-done">🏆 <b>Perfect score!</b> You found every synonym for <b>{word["base"]}</b>!</div>', unsafe_allow_html=True)
        st.balloons()
    else:
        st.markdown(f'<div class="fb-done">📋 You found <b>{found_count}</b> out of <b>{total_count}</b> synonyms for <b>{word["base"]}</b>.</div>', unsafe_allow_html=True)

    if st.session_state.found:
        st.markdown("**✅ Words you found:**")
        st.markdown(
            '<div class="chips-area">' +
            "".join(f'<span class="chip-found">{w}</span>' for w in st.session_state.found) +
            "</div>", unsafe_allow_html=True
        )
    if missed:
        st.markdown("**💛 Synonyms you missed:**")
        st.markdown(
            '<div class="chips-area">' +
            "".join(f'<span class="chip-missed">{w}</span>' for w in missed) +
            "</div>", unsafe_allow_html=True
        )
        st.markdown(f"🧠 **Remember:** all of these words mean *'{word['meaning']}'* — just like **{word['base']}**!")

    st.markdown("")
    col_next, col_reset = st.columns([1, 1])
    with col_next:
        label = "🏁 See My Results" if q_num == len(WORD_BANK) else "➡️ Next Word"
        if st.button(label):
            move_next()
            st.rerun()
    with col_reset:
        if st.button("🔄 Restart Game"):
            reset_game()
            st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    f"<p style='text-align:center;color:#9CA3AF;font-size:.85rem;'>"
    f"⭐ Total points so far: <b>{st.session_state.total_score}</b> &nbsp;|&nbsp; "
    f"The more synonyms you find, the more your vocabulary grows! 📚"
    f"</p>",
    unsafe_allow_html=True,
)
