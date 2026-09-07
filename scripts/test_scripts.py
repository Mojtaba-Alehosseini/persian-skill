#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regression tests for persian_lint.py and lookup.py.  Run:  python scripts/test_scripts.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import persian_lint as L  # noqa: E402
import lookup as K  # noqa: E402

Z = L.ZWNJ
FAILS = []


def check(name, got, want):
    if got != want:
        FAILS.append("%s\n   got:  %r\n   want: %r" % (name, got, want))


def fix(s, **kw):
    return L.normalize(s, **kw)[0]


# --- letters -----------------------------------------------------------------
check("arabic yeh/kaf", fix("كتاب و مي"), "کتاب و می")
check("teh marbuta", fix("علاقة"), "علاقه")
check("alef maksura", fix("موسى"), "موسی")
check("keeps Persian-only letters", fix("پژوهش گچ"), "پژوهش گچ")
check("keeps tanwin", fix("مثلاً بعداً"), "مثلاً بعداً")

# --- kashida -----------------------------------------------------------------
check("kashida elongation removed", fix("کتـــاب"), "کتاب")
check("spaced kashida becomes dash", fix("پر می‌کردند ـ بابا"), "پر می‌کردند – بابا")

# --- digits ------------------------------------------------------------------
check("latin digits", fix("سال 1964"), "سال ۱۹۶۴")
check("arabic-indic digits", fix("سال ١٩٦٤"), "سال ۱۹۶۴")
check("alnum token keeps latin", fix("فایل MP3 و COVID-19"), "فایل MP3 و COVID-19")
check("version protected", fix("نسخه v1.2.3 و 2.4.1"), "نسخه v1.2.3 و 2.4.1")
check("thousands comma kept", fix("قیمت 1,000 تومان"), "قیمت ۱,۰۰۰ تومان")
check("percent", fix("50% مردم"), "۵۰٪ مردم")
check("--digits keep", fix("نسخه 2 و سال 1990", digits="keep"), "نسخه ۲ و سال ۱۹۹۰".replace("۲", "2").replace("۱۹۹۰", "1990"))
check("--digits latin", fix("سال ۱۹۶۴", digits="latin"), "سال 1964")
check("url protected", fix("ببین https://x.com/a?b=1,2 را"), "ببین https://x.com/a?b=1,2 را")
check("email protected", fix("به ali.r@dtu.dk بنویس"), "به ali.r@dtu.dk بنویس")
check("code protected", fix("دستور `print(1, 2)` و ```x = 3```"), "دستور `print(1, 2)` و ```x = 3```")

# --- punctuation, Persian context only ----------------------------------------
check("comma", fix("سلام, خوبی"), "سلام، خوبی")
check("semicolon/question", fix("رفت; آمد?"), "رفت؛ آمد؟")
check("english line untouched", fix("Hello, how are you? Fine; thanks."), "Hello, how are you? Fine; thanks.")
check("mixed: english quote inside english stays", fix('He said "hi" to me.'), 'He said "hi" to me.')
check("persian quotes", fix('او گفت "سلام" و رفت'), "او گفت «سلام» و رفت")
check("curly quotes", fix("او گفت “سلام”"), "او گفت «سلام»")
check("latin word quoted in persian", fix('او گفت "hello" و رفت'), "او گفت «hello» و رفت")
check("space before comma removed", fix("رفت ، آمد"), "رفت، آمد")
check("space after comma added", fix("رفت،آمد"), "رفت، آمد")
check("no space inside guillemets", fix("« سلام »"), "«سلام»")
check("!! not split", fix("عالی!! واقعاً؟!"), "عالی!! واقعاً؟!")
check("ellipsis", fix("رفت... و آمد"), "رفت… و آمد")

# --- ZWNJ --------------------------------------------------------------------
check("mi prefix", fix("او می رود و نمی خواهم"), "او می" + Z + "رود و نمی" + Z + "خواهم")
check("mi already joined is stable", fix("می" + Z + "رود"), "می" + Z + "رود")
check("mi before digit untouched", fix("می 2"), "می ۲")
check("plural ha", fix("کتاب ها و بچه هایش"), "کتاب" + Z + "ها و بچه" + Z + "هایش")
check("ha after latin untouched", fix("PDF ها"), "PDF ها")
check("hay o hooy", fix("های و هوی"), "های و هوی")
check("superlative", fix("بزرگ ترین"), "بزرگ" + Z + "ترین")
check("comparative only suggested", fix("بزرگ تر"), "بزرگ تر")
check("heh enclitic am", fix("خانه ام و رفته اند"), "خانه" + Z + "ام و رفته" + Z + "اند")
check("heh enclitic indefinite", fix("به خانه ای رفت"), "به خانه" + Z + "ای رفت")
check("heh stopword", fix("که ای دوست"), "که ای دوست")

# --- idempotency ---------------------------------------------------------------
messy = 'او مي رود و كتاب ها روي ميز است ، و بزرگ ترين آرزو همين بود 1964 . گفت "خوب" ; چرا?'
once = fix(messy)
check("idempotent", fix(once), once)
check("eval-4 sample", once,
      "او می" + Z + "رود و کتاب" + Z + "ها روی میز است، و بزرگ" + Z + "ترین آرزو همین بود ۱۹۶۴. گفت «خوب»؛ چرا؟")

# --- suggestions ---------------------------------------------------------------
s = L.suggestions("زمینِ تر بود و میرود و میز")
types = [x["type"] for x in s]
check("suggest tar", "maybe_comparative_tar" in types, True)
check("suggest glued mi once (not میز)", types.count("maybe_glued_mi"), 1)
check("em dash flagged", any(x["type"] == "em_dash" for x in L.suggestions("رفت — آمد")), True)
st = L.suggestions("این کتاب دارای سه فصل می‌باشد و توسط او نوشته شد.", style=True)
check("style flags", sorted({x["hint"][:6] for x in st if x["type"] == "style"}),
      sorted({"«می‌با", "«دارای", "«توسط»"}))
check("no style flags without --style", any(x["type"] == "style" for x in L.suggestions("می‌باشد")), False)

# --- lookup --------------------------------------------------------------------
rows = K.load("idioms.tsv")
check("bank loads", len(rows) > 20, True)
hit = K.find_en(rows, "It cost an arm and a leg, so let's break the ice.")
check("idiom hits", sorted(h[0] for h in hit), ["break the ice", "cost an arm and a leg"])
g = K.load("glossary.tsv")
check("inflected multiword", any(h[0] == "business partner" for h in K.find_en(g, "my business partners")), True)
check("AI does not match aid", any(h[0] == "AI" for h in K.find_en(g, "first aid kit")), False)
check("AI matches AI", any(h[0] == "AI" for h in K.find_en(g, "AI tools")), True)
check("no false positive", K.find_en(rows, "The weather is nice today."), [])
check("reverse", any(h[0] == "the lights went out" for h in K.find_fa(g, "همزمان برق رفت")), True)

# --- mixed documents (line-aware) ------------------------------------------------
check("english line keeps digits", fix("Phase 3 uses P8 and «چرا» twice."), "Phase 3 uses P8 and «چرا» twice.")
check("english list of persian words keeps commas", fix("Use ZWNJ in (RTL, نیم‌فاصله, digits)."), "Use ZWNJ in (RTL, نیم‌فاصله, digits).")
check("persian words flanking comma in english doc", fix("word سلام, خوبی word word word"), "word سلام، خوبی word word word")
check("list marker keeps latin digit", fix("1. کتاب ها را بخوان"), "1. کتاب" + Z + "ها را بخوان")
check("indentation preserved", fix("    کد تو رفتگی\n  - آیتم"), "    کد تو رفتگی\n  - آیتم")
check("number-only line in persian doc", fix("سلام دنیا\n1964\nخداحافظ"), "سلام دنیا\n۱۹۶۴\nخداحافظ")
check("number-only line in english doc", fix("hello world\n1964\nbye"), "hello world\n1964\nbye")
check("english quote near persian stays", fix('- "Isn\'t 1947 the date?" → «مگر … نیست؟»'), '- "Isn\'t 1947 the date?" → «مگر … نیست؟»')
check("persian majority quote on english line", fix('the word "کتاب ها" means books'), 'the word «کتاب' + Z + 'ها» means books')
check("english period spacing untouched", fix("end . next"), "end . next")
check("persian period spacing fixed", fix("رفت . آمد"), "رفت. آمد")
check("idempotent mixed", fix(fix("Phase 3: سلام, خوبی? 1. item")), fix("Phase 3: سلام, خوبی? 1. item"))
check("indented code line protected", fix("    python x.py --fix  file.txt   # سلام"), "    python x.py --fix  file.txt   # سلام")
check("english list of marks keeps spaces", fix("no space before ، ؛ ؟ in Persian"), "no space before ، ؛ ؟ in Persian")
check("persian phrase in english line still fixed", fix("the phrase «سلام ، خوبی» means hi"), "the phrase «سلام، خوبی» means hi")

if FAILS:
    print("FAILED %d test(s):" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("all tests passed")
