"""
LinguaDetect: сайт определения языка (Gradio).
Модель обучена в Colab (TF-IDF + LinearSVC на WiLI-2018) и лежит рядом: linguadetect_model.joblib
Запуск локально:  python app.py
"""

import os
from pathlib import Path

import joblib

import gradio as gr
import html

LANGUAGES = {
    "rus": "Russian",
    "eng": "English",
    "deu": "German",
    "fra": "French",
    "spa": "Spanish",
    "ita": "Italian",
    "por": "Portuguese",
    "nld": "Dutch",
    "pol": "Polish",
    "tur": "Turkish"
}

SUPPORTED_LANGUAGES = [
    ("🇷🇺", "Russian", "Русский"),
    ("🇬🇧", "English", "Английский"),
    ("🇩🇪", "German", "Немецкий"),
    ("🇫🇷", "French", "Французский"),
    ("🇪🇸", "Spanish", "Испанский"),
    ("🇮🇹", "Italian", "Итальянский"),
    ("🇵🇹", "Portuguese", "Португальский"),
    ("🇳🇱", "Dutch", "Нидерландский"),
    ("🇵🇱", "Polish", "Польский"),
    ("🇹🇷", "Turkish", "Турецкий")
]

print("LinguaDetect supports", len(LANGUAGES), "languages")

# ============ МОДЕЛЬ ============
MODEL_PATH = Path(__file__).parent / "linguadetect_model.joblib"
model = joblib.load(MODEL_PATH)

def detect_language(text):

    if not isinstance(text, str) or not text.strip():
        return "Please enter a valid text."

    prediction = model.predict([text])[0]

    return LANGUAGES.get(
        prediction,
        "Unknown language"
    )


print("Language detection function is ready!")

def run_detection(text):

    if not isinstance(text, str) or not text.strip():
        return (
            "Please enter some text.",
            "Your result will appear here."
        )

    detected = detect_language(text.strip())

    if detected == "Please enter a valid text.":
        return (
            detected,
            "Try entering a longer text."
        )

    return (
        detected,
        f"LinguaDetect identified the language as **{detected}**."
    )

print("Detection function is ready!")

# ============ ДИЗАЙН: бежевая тема, меню-ссылки, панель настроек ============

custom_css = """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Lora:wght@500;600;700&display=swap');

/* ---------- переменные темы (меняются панелью настроек) ---------- */
:root {
    --ld-bg: #F3ECE0;
    --ld-surface: #FBF7F0;
    --ld-surface-2: #EFE5D4;
    --ld-border: #E3D6C1;
    --ld-text: #3B2F26;
    --ld-muted: #8A7A69;
    --ld-accent: #B86B4B;
    --ld-on-accent: #FFFFFF;
    --ld-radius: 18px;
    --ld-gap: 1;
    --ld-fs: 16px;
    --ld-font-body: 'DM Sans', system-ui, sans-serif;
    --ld-font-head: 'Lora', Georgia, serif;
    --ld-shadow: 0 8px 24px rgba(90, 64, 40, .08);
}

:root[data-theme="dark"] {
    --ld-bg: #221C17;
    --ld-surface: #2D251F;
    --ld-surface-2: #382E26;
    --ld-border: #4A3E33;
    --ld-text: #F0E6D6;
    --ld-muted: #B3A28D;
    --ld-shadow: 0 8px 24px rgba(0, 0, 0, .35);
}

:root[data-font="serif"] {
    --ld-font-body: 'Lora', Georgia, serif;
}

/* ---------- подмена цветов Gradio на наши ---------- */
body { background: var(--ld-bg) !important; }

html body .gradio-container {
    --body-background-fill: var(--ld-bg);
    --background-fill-primary: var(--ld-surface);
    --background-fill-secondary: var(--ld-surface-2);
    --block-background-fill: var(--ld-surface);
    --block-border-color: var(--ld-border);
    --border-color-primary: var(--ld-border);
    --input-background-fill: var(--ld-surface);
    --input-border-color: var(--ld-border);
    --body-text-color: var(--ld-text);
    --body-text-color-subdued: var(--ld-muted);
    --block-label-text-color: var(--ld-muted);
    --block-title-text-color: var(--ld-muted);
    --button-primary-background-fill: var(--ld-accent);
    --button-primary-background-fill-hover: color-mix(in srgb, var(--ld-accent) 85%, black);
    --button-primary-text-color: var(--ld-on-accent);
    --button-primary-border-color: transparent;
    --button-secondary-background-fill: var(--ld-surface-2);
    --button-secondary-background-fill-hover: var(--ld-border);
    --button-secondary-text-color: var(--ld-text);
    --color-accent: var(--ld-accent);
    --link-text-color: var(--ld-accent);
    --block-radius: var(--ld-radius);
    --input-radius: calc(var(--ld-radius) * .7);
    --button-large-radius: calc(var(--ld-radius) * .7);
    --text-sm: calc(var(--ld-fs) * .9);
    --text-md: var(--ld-fs);
    --text-lg: calc(var(--ld-fs) * 1.12);
    --font: var(--ld-font-body);
    max-width: 1150px !important;
    margin: auto !important;
    font-family: var(--ld-font-body) !important;
    font-size: var(--ld-fs) !important;
    color: var(--ld-text) !important;
    background: transparent !important;
}

#main { max-width: 1050px; margin: auto; }

/* якоря: чтобы заголовок не прятался под меню */
#detector, #languages, #how, #features, #about { scroll-margin-top: 90px; }

/* ---------- гиперссылки ---------- */
.gradio-container a.ld-link {
    color: var(--ld-text);
    text-decoration: none;
    font-weight: 600;
    background: linear-gradient(var(--ld-accent), var(--ld-accent)) 0 100% / 0 2px no-repeat;
    transition: background-size .25s ease, color .2s ease;
    padding-bottom: 2px;
}
.gradio-container a.ld-link:hover,
.gradio-container a.ld-link:focus-visible {
    color: var(--ld-accent);
    background-size: 100% 2px;
    outline: none;
}

/* ---------- меню ---------- */
#topnav {
    position: sticky;
    top: 10px;
    z-index: 50;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    gap: 8px 22px;
    padding: 12px 24px;
    margin: 12px 0 18px;
    background: color-mix(in srgb, var(--ld-surface) 88%, transparent);
    backdrop-filter: blur(8px);
    border: 1px solid var(--ld-border);
    border-radius: 999px;
    box-shadow: var(--ld-shadow);
}
#topnav .brand {
    font-family: var(--ld-font-head);
    font-weight: 700;
    font-size: 1.15em;
    margin-right: 10px;
    color: var(--ld-text);
}

/* ---------- hero ---------- */
#hero {
    background: linear-gradient(135deg,
        color-mix(in srgb, var(--ld-accent) 24%, var(--ld-surface)),
        var(--ld-surface-2));
    color: var(--ld-text);
    border: 1px solid var(--ld-border);
    padding: calc(55px * var(--ld-gap)) 35px;
    border-radius: calc(var(--ld-radius) * 1.4);
    text-align: center;
    margin: 10px 0 20px;
}
#hero h1 {
    font-family: var(--ld-font-head);
    font-size: clamp(34px, 6vw, 52px);
    margin: 6px 0 10px;
    color: var(--ld-text);
}
#hero p { font-size: 1.1em; color: var(--ld-muted); margin: 0; }
#hero .tag {
    color: var(--ld-accent);
    letter-spacing: 2px;
    font-size: 12px;
    font-weight: 700;
}

/* ---------- блоки ---------- */
#detector {
    background: var(--ld-surface);
    padding: calc(28px * var(--ld-gap));
    border-radius: var(--ld-radius);
    border: 1px solid var(--ld-border);
    box-shadow: var(--ld-shadow);
}
#detect-btn button { min-height: 48px; font-weight: 700; }
#result {
    background: var(--ld-surface-2);
    border-radius: calc(var(--ld-radius) * .7);
    padding: 15px;
}

.section-title {
    color: var(--ld-text);
    font-family: var(--ld-font-head);
    font-size: 1.9em;
    margin: calc(45px * var(--ld-gap)) 0 10px;
}
.section-subtitle { color: var(--ld-muted); margin-bottom: 20px; }

.ld-grid-langs {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(145px, 1fr));
    gap: calc(14px * var(--ld-gap));
}
.ld-grid-info {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: calc(16px * var(--ld-gap));
}

.language-card, .info-card {
    background: var(--ld-surface);
    border: 1px solid var(--ld-border);
    border-radius: var(--ld-radius);
    box-shadow: var(--ld-shadow);
}
.language-card {
    padding: calc(18px * var(--ld-gap)) 10px;
    text-align: center;
    transition: transform .2s ease, border-color .2s ease;
}
.language-card:hover { transform: translateY(-3px); border-color: var(--ld-accent); }
.language-flag { font-size: 30px; margin-bottom: 8px; }
.language-name { font-weight: 700; color: var(--ld-text); }
.language-translation { color: var(--ld-muted); font-size: .85em; }

.info-card { padding: calc(22px * var(--ld-gap)); height: 100%; }
.info-card h3 { color: var(--ld-accent); font-family: var(--ld-font-head); margin-top: 0; }
.info-card p { color: var(--ld-muted); line-height: 1.65; }

#footer {
    background: var(--ld-surface-2);
    border: 1px solid var(--ld-border);
    color: var(--ld-text);
    text-align: center;
    padding: calc(25px * var(--ld-gap));
    border-radius: var(--ld-radius);
    margin-top: 40px;
}
#footer h2 { font-family: var(--ld-font-head); margin-top: 0; }
#footer p { color: var(--ld-muted); }
#footer .links { display: flex; flex-wrap: wrap; gap: 8px 22px; justify-content: center; }

textarea { border-radius: calc(var(--ld-radius) * .7) !important; }

/* ---------- кнопка и панель настроек ---------- */
#ld-gear {
    position: fixed; right: 18px; bottom: 18px; z-index: 9999;
    width: 50px; height: 50px; border-radius: 50%;
    border: 1px solid var(--ld-border);
    background: var(--ld-surface); color: var(--ld-text);
    font-size: 24px; line-height: 1; cursor: pointer;
    box-shadow: var(--ld-shadow);
    transition: transform .3s ease;
}
#ld-gear:hover { transform: rotate(60deg); }

#ld-panel {
    position: fixed; right: 18px; bottom: 80px; z-index: 9999;
    width: min(330px, calc(100vw - 36px)); max-height: 72vh; overflow: auto;
    background: var(--ld-surface); color: var(--ld-text);
    border: 1px solid var(--ld-border); border-radius: var(--ld-radius);
    box-shadow: var(--ld-shadow); padding: 18px;
    display: none; font-family: var(--ld-font-body); font-size: 14px;
}
#ld-panel.open { display: block; }
#ld-panel h4 { margin: 0 0 14px; font-family: var(--ld-font-head); font-size: 18px; }
.ld-row { margin: 0 0 14px; }
.ld-label {
    font-size: 11px; letter-spacing: .09em; text-transform: uppercase;
    color: var(--ld-muted); margin-bottom: 6px;
}
.ld-seg { display: flex; gap: 6px; flex-wrap: wrap; }
.ld-seg button {
    flex: 1; padding: 8px 10px; border-radius: 999px;
    border: 1px solid var(--ld-border); background: var(--ld-surface-2);
    color: var(--ld-text); cursor: pointer; font: inherit;
}
.ld-seg button.on { background: var(--ld-accent); color: var(--ld-on-accent); border-color: transparent; }
.ld-sw button { width: 30px; height: 30px; flex: none; padding: 0; border-radius: 50%; }
.ld-sw button.on { outline: 3px solid var(--ld-text); outline-offset: 2px; }
#ld-reset {
    width: 100%; padding: 9px; border-radius: 999px; cursor: pointer; font: inherit;
    border: 1px solid var(--ld-border); background: transparent; color: var(--ld-muted);
}
#ld-reset:hover { color: var(--ld-accent); border-color: var(--ld-accent); }

@media (max-width: 600px) {
    #hero { padding: 35px 18px; }
    #detector { padding: 16px; }
    #topnav { border-radius: var(--ld-radius); }
}
"""

# ---------- JavaScript: настройки + плавная прокрутка ----------
custom_js = """
(function () {
  var KEY = 'linguadetect-settings';
  var DEFAULTS = { theme: 'light', accent: '#B86B4B', size: '16', font: 'sans', radius: '18', density: '1' };
  var s = {};
  for (var k in DEFAULTS) { s[k] = DEFAULTS[k]; }
  try {
    var saved = JSON.parse(localStorage.getItem(KEY) || '{}');
    for (var k2 in saved) { if (k2 in DEFAULTS) { s[k2] = saved[k2]; } }
  } catch (e) {}

  function apply() {
    var r = document.documentElement;
    r.setAttribute('data-theme', s.theme);
    r.setAttribute('data-font', s.font);
    r.style.setProperty('--ld-accent', s.accent);
    r.style.setProperty('--ld-fs', s.size + 'px');
    r.style.setProperty('--ld-radius', s.radius + 'px');
    r.style.setProperty('--ld-gap', s.density);
  }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) {} }
  apply();

  var OPT = {
    theme:   [['light', 'Light'], ['dark', 'Dark']],
    size:    [['14', 'S'], ['16', 'M'], ['18', 'L']],
    font:    [['sans', 'Sans'], ['serif', 'Serif']],
    radius:  [['6', 'Sharp'], ['18', 'Soft'], ['30', 'Round']],
    density: [['0.8', 'Compact'], ['1', 'Normal'], ['1.3', 'Airy']]
  };
  var TITLES = { theme: 'Theme', size: 'Text size', font: 'Font', radius: 'Corners', density: 'Spacing' };
  var ACCENTS = [['#B86B4B', 'Terracotta'], ['#6F8F72', 'Sage'], ['#8A7BB0', 'Lavender'], ['#C27C88', 'Powder rose']];

  function build() {
    if (document.getElementById('ld-gear')) { return; }
    var gear = document.createElement('button');
    gear.id = 'ld-gear';
    gear.type = 'button';
    gear.setAttribute('aria-label', 'Settings');
    gear.textContent = '\\u2699';

    var panel = document.createElement('div');
    panel.id = 'ld-panel';
    var h = '<h4>Settings</h4>';
    h += '<div class="ld-row"><div class="ld-label">Accent color</div><div class="ld-seg ld-sw">';
    ACCENTS.forEach(function (a) {
      h += '<button type="button" data-k="accent" data-v="' + a[0] + '" title="' + a[1] +
           '" aria-label="' + a[1] + '" style="background:' + a[0] + '"></button>';
    });
    h += '</div></div>';
    Object.keys(OPT).forEach(function (key) {
      h += '<div class="ld-row"><div class="ld-label">' + TITLES[key] + '</div><div class="ld-seg">';
      OPT[key].forEach(function (o) {
        h += '<button type="button" data-k="' + key + '" data-v="' + o[0] + '">' + o[1] + '</button>';
      });
      h += '</div></div>';
    });
    h += '<button type="button" id="ld-reset">Reset to default</button>';
    panel.innerHTML = h;

    document.body.appendChild(gear);
    document.body.appendChild(panel);

    function refresh() {
      var btns = panel.querySelectorAll('button[data-k]');
      for (var i = 0; i < btns.length; i++) {
        var b = btns[i];
        b.classList.toggle('on', s[b.getAttribute('data-k')] === b.getAttribute('data-v'));
      }
    }
    refresh();

    gear.addEventListener('click', function () { panel.classList.toggle('open'); });
    panel.addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b) { return; }
      if (b.id === 'ld-reset') {
        for (var k in DEFAULTS) { s[k] = DEFAULTS[k]; }
      } else if (b.getAttribute('data-k')) {
        s[b.getAttribute('data-k')] = b.getAttribute('data-v');
      } else { return; }
      apply(); save(); refresh();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { panel.classList.remove('open'); }
    });
  }

  // плавная прокрутка по ссылкам меню
  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[data-scroll]') : null;
    if (!a) { return; }
    e.preventDefault();
    var id = a.getAttribute('data-scroll');
    if (id === 'top') { window.scrollTo({ top: 0, behavior: 'smooth' }); return; }
    var el = document.getElementById(id);
    if (el) { el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else { build(); }
})();
"""

head_html = "<script>" + custom_js + "</script>"

print("Design styles and settings panel are ready!")

# ============ СЕКЦИИ САЙТА (с якорями и гиперссылками) ============

DATASET_URL_PAGE = "https://zenodo.org/records/841984"
SKLEARN_URL = "https://scikit-learn.org/stable/"

nav_html = """
<nav id="topnav">
    <span class="brand">✦ LinguaDetect</span>
    <a class="ld-link" href="#detector"  data-scroll="detector">Detector</a>
    <a class="ld-link" href="#languages" data-scroll="languages">Languages</a>
    <a class="ld-link" href="#how"       data-scroll="how">How it works</a>
    <a class="ld-link" href="#features"  data-scroll="features">Features</a>
    <a class="ld-link" href="#about"     data-scroll="about">About</a>
    <a class="ld-link" href="__DATASET__" target="_blank" rel="noopener noreferrer">Dataset ↗</a>
</nav>
""".replace("__DATASET__", DATASET_URL_PAGE)

hero_html = """
<div id="hero">
    <div class="tag">AI-POWERED LANGUAGE IDENTIFICATION</div>
    <h1>✦ LinguaDetect</h1>
    <p>One text. One click. Discover the language.</p>
</div>
"""

language_cards = ""

for flag, name, translation in SUPPORTED_LANGUAGES:
    language_cards += f"""
    <div class="language-card">
        <div class="language-flag">{flag}</div>
        <div class="language-name">{name}</div>
        <div class="language-translation">{translation}</div>
    </div>
    """

languages_html = f"""
<div class="section-title" id="languages">Supported Languages</div>

<p class="section-subtitle">
    LinguaDetect can identify text written in these 10 languages.
</p>

<div class="ld-grid-langs">
    {language_cards}
</div>
"""

how_it_works = """
<div class="section-title" id="how">How It Works</div>

<p class="section-subtitle">
    Three simple steps to identify a language.
    <a class="ld-link" href="#detector" data-scroll="detector">Try it now ↑</a>
</p>

<div class="ld-grid-info">
    <div class="info-card">
        <h3>01. Enter Text</h3>
        <p>Type or paste a text sample into the input field.</p>
    </div>

    <div class="info-card">
        <h3>02. Analyze</h3>
        <p>
            Our machine learning model analyzes the text
            using TF-IDF features and LinearSVC.
        </p>
    </div>

    <div class="info-card">
        <h3>03. Get Result</h3>
        <p>LinguaDetect identifies the language and displays the result.</p>
    </div>
</div>
"""

features_html = """
<div class="section-title" id="features">Features</div>

<p class="section-subtitle">What makes LinguaDetect useful?</p>

<div class="ld-grid-info">
    <div class="info-card">
        <h3>10 Languages</h3>
        <p>
            Supports Russian, English, German, French,
            Spanish, Italian, Portuguese, Dutch,
            Polish and Turkish.
        </p>
    </div>

    <div class="info-card">
        <h3>Machine Learning</h3>
        <p>
            Uses a LinearSVC classification model
            with TF-IDF feature extraction.
        </p>
    </div>

    <div class="info-card">
        <h3>Simple Interface</h3>
        <p>An easy-to-use interface for quick language identification.</p>
    </div>

    <div class="info-card">
        <h3>Fast Detection</h3>
        <p>Get a language prediction after submitting your text.</p>
    </div>
</div>
"""

about_html = """
<div class="section-title" id="about">About LinguaDetect</div>

<div class="info-card">
    <h3>About the Project</h3>

    <p>
        LinguaDetect is a machine learning project
        designed to identify the language of a given text.
        It was developed using the
        <a class="ld-link" href="__DATASET__" target="_blank" rel="noopener noreferrer">WiLI-2018 dataset ↗</a>.
    </p>

    <p>
        The system uses TF-IDF for text feature extraction
        and LinearSVC (from
        <a class="ld-link" href="__SKLEARN__" target="_blank" rel="noopener noreferrer">scikit-learn ↗</a>)
        for language classification.
    </p>

    <p>
        The project currently supports 10 languages
        and provides a simple interface for users.
    </p>
</div>
""".replace("__DATASET__", DATASET_URL_PAGE).replace("__SKLEARN__", SKLEARN_URL)

footer_html = """
<div id="footer">
    <h2>LinguaDetect</h2>
    <p>TF-IDF + LinearSVC | 10 Supported Languages</p>
    <p>Machine Learning Language Identification</p>
    <div class="links">
        <a class="ld-link" href="#top" data-scroll="top">Back to top ↑</a>
        <a class="ld-link" href="#about" data-scroll="about">About</a>
        <a class="ld-link" href="__DATASET__" target="_blank" rel="noopener noreferrer">WiLI-2018 ↗</a>
        <a class="ld-link" href="__SKLEARN__" target="_blank" rel="noopener noreferrer">scikit-learn ↗</a>
    </div>
</div>
""".replace("__DATASET__", DATASET_URL_PAGE).replace("__SKLEARN__", SKLEARN_URL)

print("All sections are ready!")

# ============ ГОРЯЧИЕ КЛАВИШИ ============

hotkeys_css = """
#ld-keys {
    position: fixed; right: 78px; bottom: 18px; z-index: 9999;
    height: 50px; min-width: 50px; padding: 0 14px; border-radius: 999px;
    border: 1px solid var(--ld-border);
    background: var(--ld-surface); color: var(--ld-text);
    font-size: 20px; line-height: 1; cursor: pointer;
    box-shadow: var(--ld-shadow);
}
#ld-keys:hover { border-color: var(--ld-accent); }

#ld-help {
    position: fixed; inset: 0; z-index: 10000;
    display: none; align-items: center; justify-content: center;
    background: rgba(40, 30, 22, .45);
}
#ld-help.open { display: flex; }
#ld-help .box {
    background: var(--ld-surface); color: var(--ld-text);
    border: 1px solid var(--ld-border); border-radius: var(--ld-radius);
    box-shadow: var(--ld-shadow); padding: 22px 24px;
    width: min(420px, calc(100vw - 36px)); max-height: 80vh; overflow: auto;
    font-family: var(--ld-font-body); font-size: 14px;
}
#ld-help h4 { margin: 0 0 12px; font-family: var(--ld-font-head); font-size: 20px; }
#ld-help .row {
    display: flex; justify-content: space-between; align-items: center; gap: 16px;
    padding: 8px 0; border-bottom: 1px solid var(--ld-border);
}
#ld-help .row:last-of-type { border-bottom: none; }
#ld-help kbd {
    background: var(--ld-surface-2); border: 1px solid var(--ld-border);
    border-radius: 6px; padding: 2px 8px; white-space: nowrap;
    font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 12.5px;
}
#ld-help .hint { color: var(--ld-muted); font-size: 12px; margin-top: 12px; }

@media (hover: none) { #ld-keys { display: none; } }
"""

hotkeys_js = r"""
(function () {
  if (window.__ldKeys) { return; }
  window.__ldKeys = true;

  // Используем e.code (физическая клавиша), поэтому всё работает и на русской раскладке.
  var SECTIONS = { Digit1: 'detector', Digit2: 'languages', Digit3: 'how', Digit4: 'features', Digit5: 'about' };
  var SIZES = [14, 16, 18];
  var HELP = [
    ['Ctrl / \u2318 + Enter', 'Detect language'],
    ['/', 'Focus the text field'],
    ['C', 'Clear'],
    ['1 \u2013 5', 'Jump to a section'],
    ['0', 'Back to top'],
    ['T', 'Light / dark theme'],
    ['S', 'Open settings'],
    ['+ / \u2212', 'Text size'],
    ['?', 'Show this help'],
    ['Esc', 'Close panels']
  ];

  function isTyping(el) {
    if (!el) { return false; }
    var t = (el.tagName || '').toUpperCase();
    return t === 'INPUT' || t === 'TEXTAREA' || t === 'SELECT' || !!el.isContentEditable;
  }
  function textField() {
    return document.querySelector('#detector textarea[placeholder^="Type or paste"]') ||
           document.querySelector('#detector textarea');
  }
  function clickById(id) {
    var el = document.getElementById(id);
    if (!el) { return; }
    var b = el.tagName === 'BUTTON' ? el : el.querySelector('button');
    if (b) { b.click(); }
  }
  function clearAll() {
    var btns = document.querySelectorAll('#detector button');
    for (var i = 0; i < btns.length; i++) {
      if (btns[i].textContent.trim() === 'Clear') { btns[i].click(); break; }
    }
    var f = textField();
    if (f) { f.focus(); }
  }
  function setOpt(k, v) {
    var b = document.querySelector('#ld-panel button[data-k="' + k + '"][data-v="' + v + '"]');
    if (b) { b.click(); }
  }
  function toggleTheme() {
    var dark = document.documentElement.getAttribute('data-theme') === 'dark';
    setOpt('theme', dark ? 'light' : 'dark');
  }
  function changeSize(step) {
    var cur = parseInt(document.documentElement.style.getPropertyValue('--ld-fs'), 10) || 16;
    var i = SIZES.indexOf(cur);
    if (i < 0) { i = 1; }
    i = Math.max(0, Math.min(SIZES.length - 1, i + step));
    setOpt('size', String(SIZES[i]));
  }
  function goTo(id) {
    var el = document.getElementById(id);
    if (el) { el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
  }
  function toggleSettings() {
    var g = document.getElementById('ld-gear');
    if (g) { g.click(); }
  }
  function helpEl() { return document.getElementById('ld-help'); }
  function openHelp() { var h = helpEl(); if (h) { h.classList.add('open'); } }
  function closeHelp() { var h = helpEl(); if (h) { h.classList.remove('open'); } }

  function build() {
    if (document.getElementById('ld-keys')) { return; }

    var btn = document.createElement('button');
    btn.id = 'ld-keys';
    btn.type = 'button';
    btn.setAttribute('aria-label', 'Keyboard shortcuts');
    btn.title = 'Keyboard shortcuts (?)';
    btn.textContent = '\u2328';

    var help = document.createElement('div');
    help.id = 'ld-help';
    var h = '<div class="box"><h4>Keyboard shortcuts</h4>';
    HELP.forEach(function (r) {
      h += '<div class="row"><span>' + r[1] + '</span><kbd>' + r[0] + '</kbd></div>';
    });
    h += '<div class="hint">Single-key shortcuts work when you are not typing in a field.</div></div>';
    help.innerHTML = h;

    document.body.appendChild(btn);
    document.body.appendChild(help);

    btn.addEventListener('click', openHelp);
    help.addEventListener('click', function (e) { if (e.target === help) { closeHelp(); } });
  }

  document.addEventListener('keydown', function (e) {
    var typing = isTyping(e.target);

    // Ctrl/Cmd + Enter работает даже внутри текстового поля
    if ((e.ctrlKey || e.metaKey) && (e.code === 'Enter' || e.code === 'NumpadEnter')) {
      e.preventDefault();
      clickById('detect-btn');
      return;
    }

    if (e.code === 'Escape') {
      closeHelp();
      if (typing && e.target.blur) { e.target.blur(); }
      return;
    }

    // Одиночные клавиши: только когда не печатаем и нет модификаторов
    if (typing || e.ctrlKey || e.metaKey || e.altKey) { return; }

    var c = e.code;
    if (c === 'Slash' && e.shiftKey) { e.preventDefault(); openHelp(); return; }
    if (c === 'Slash') {
      e.preventDefault();
      goTo('detector');
      var f = textField();
      if (f) { f.focus(); }
      return;
    }
    if (SECTIONS[c]) { e.preventDefault(); goTo(SECTIONS[c]); return; }
    if (c === 'Digit0') { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); return; }
    if (c === 'KeyC') { e.preventDefault(); clearAll(); return; }
    if (c === 'KeyT') { e.preventDefault(); toggleTheme(); return; }
    if (c === 'KeyS') { e.preventDefault(); toggleSettings(); return; }
    if (c === 'Equal' || c === 'NumpadAdd') { e.preventDefault(); changeSize(1); return; }
    if (c === 'Minus' || c === 'NumpadSubtract') { e.preventDefault(); changeSize(-1); return; }
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else { build(); }
})();
"""

# защита от двойного запуска ячейки
if "__ldKeys" not in custom_js:
    custom_css += hotkeys_css
    custom_js += hotkeys_js
    head_html = "<script>" + custom_js + "</script>"

print("Hotkeys added! Now run the 'Сборка и запуск сайта' cell.")

# ============ СБОРКА И ЗАПУСК ИНТЕРФЕЙСА ============
import inspect

# В Gradio 6 параметры css/head переехали из gr.Blocks() в launch().
# Этот код работает в обеих версиях: сам определяет, куда их передать.
_blocks_params = inspect.signature(gr.Blocks.__init__).parameters
_launch_params = inspect.signature(gr.Blocks.launch).parameters

_design = {"css": custom_css, "head": head_html}
blocks_kwargs = {k: v for k, v in _design.items() if k in _blocks_params}
launch_kwargs = {
    k: v for k, v in _design.items()
    if k not in _blocks_params and k in _launch_params
}

with gr.Blocks(title="LinguaDetect", **blocks_kwargs) as demo:

    with gr.Column(elem_id="main"):

        # МЕНЮ + HERO
        gr.HTML('<a id="top"></a>' + nav_html + hero_html)

        # ДЕТЕКТОР
        with gr.Column(elem_id="detector"):

            gr.Markdown("## Identify a Language")
            gr.Markdown("Enter your text below to discover its language.")

            text_input = gr.Textbox(
                label="Your text",
                placeholder="Type or paste your text here...",
                lines=6,
                max_lines=12
            )

            with gr.Row():
                detect_button = gr.Button(
                    "Detect Language",
                    variant="primary",
                    elem_id="detect-btn"
                )
                clear_button = gr.ClearButton(value="Clear")

            detected_language = gr.Textbox(
                label="Detected Language",
                interactive=False
            )

            result_message = gr.Markdown(elem_id="result")

            clear_button.add([text_input, detected_language, result_message])

        # ПРИМЕРЫ
        gr.Markdown("## Try These Examples")

        gr.Examples(
            examples=[
                ["Hello! How are you today?"],
                ["Привет! Как твои дела?"],
                ["Hallo! Wie geht es dir?"],
                ["Bonjour! Comment allez-vous?"],
                ["¡Hola! ¿Cómo estás?"],
                ["Ciao! Come stai?"],
                ["Olá! Como você está?"],
                ["Hallo! Hoe gaat het met je?"],
                ["Cześć! Jak się masz?"],
                ["Merhaba! Nasılsın?"]
            ],
            inputs=text_input
        )

        # ОСТАЛЬНЫЕ СЕКЦИИ
        gr.HTML(languages_html)
        gr.HTML(how_it_works)
        gr.HTML(features_html)
        gr.HTML(about_html)
        gr.HTML(footer_html)

    # КНОПКА И ENTER
    detect_button.click(
        fn=run_detection,
        inputs=text_input,
        outputs=[detected_language, result_message]
    )

    text_input.submit(
        fn=run_detection,
        inputs=text_input,
        outputs=[detected_language, result_message]
    )

print("LinguaDetect interface created successfully!")
print("Gradio version:", gr.__version__)

# На Render порт приходит из переменной окружения PORT; локально по умолчанию 7860
demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860)),
    show_error=True,
    **launch_kwargs
)
