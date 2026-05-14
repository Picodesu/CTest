#!/usr/bin/env python3
"""
CTEST DAILY CODE FORTUNE GENERATOR
====================================
每日代码运势占卜器 - 程序员的赛博护身符

用法: python fortune.py [--lang zh|en|ja|ko|all]

灵感来源：命运的不可预测性与 git push 的勇气
"""

import hashlib
import sys
from datetime import datetime

FORTUNES_ZH = [
    "今日宜: 重构旧代码。忌: 在周五下午 deploy。",
    "一段被遗忘的代码将在今日重见天日。它会让你哭泣。",
    "你的下一次 commit message 将成为传世名言。",
    "今日 bug 数: 0（因为还没开始写代码）。",
    "好运代码语言: Python。坏运代码语言: 你自己写的。",
    "一位神秘的 code reviewer 将在 PR 中留下改变你人生的评论。",
    "今日适合: 写注释。明日适合: 读懂今天写的注释。",
    "警告: 你即将 git push --force 到 main。请三思。",
    "今天的你，是昨天的你计划中的明天的你。而代码还是昨天的。",
    "一段 3 行的代码将解决困扰你三天的问题。",
    "今日五行缺: Stack Overflow。",
    "你的代码质量与今日咖啡浓度成正比。",
]

FORTUNES_EN = [
    "Today: refactor old code. Avoid: deploying on Friday afternoon.",
    "A forgotten piece of code will resurface today. It will make you cry.",
    "Your next commit message will become a legendary quote.",
    "Today's bug count: 0 (because you haven't started coding yet).",
    "Lucky language: Python. Unlucky language: whatever you wrote yesterday.",
    "A mysterious code reviewer will leave a life-changing comment on your PR.",
    "Today is for writing comments. Tomorrow is for understanding them.",
    "Warning: you are about to git push --force to main. Think twice.",
    "You today are the you that yesterday's you planned for tomorrow. The code is still from yesterday.",
    "3 lines of code will solve the problem that haunted you for 3 days.",
    "Today's elemental deficiency: Stack Overflow.",
    "Your code quality is directly proportional to today's coffee concentration.",
]

FORTUNES_JA = [
    "今日やるべきこと: 古いコードのリファクタリング。避けるべきこと: 金曜日のデプロイ。",
    "忘れられたコードが今日蘇ります。泣くでしょう。",
    "次のコミットメッセージは名言になるでしょう。",
    "今日のバグ数: 0（まだコードを書いていないから）。",
    "ラッキーランゲージ: Python。アンラッキー: 昨日あなたが書いたもの。",
    "謎のレビュアーがPRに人生を変えるコメントを残すでしょう。",
    "今日のテーマ: コメントを書く。明日のテーマ: 今日書いたコメントを読む。",
    "警告: git push --force を main に実行しようとしています。よく考えてください。",
    "今日のあなたは昨日のあなたが計画した明日のあなた。コードは昨日のまま。",
    "3行のコードが3日間悩ませた問題を解決します。",
    "今日の不足エレメント: Stack Overflow。",
    "コードの品質は今日のコーヒー濃度に比例します。",
]

FORTUNES_KO = [
    "오늘 할 일: 오래된 코드 리팩토링. 피할 일: 금요일 배포.",
    "잊혀진 코드가 오늘 되살아납니다. 우실 겁니다.",
    "다음 커밋 메시지는 명언이 될 것입니다.",
    "오늘의 버그 수: 0 (아직 코드를 안 써서).",
    "행운의 언어: Python. 불운의 언어: 어제 당신이 쓴 것.",
    "수수께끼의 리뷰어가 PR에 인생을 바꿀 댓글을 남길 것입니다.",
    "오늘은 주석을 쓰는 날. 내일은 오늘 쓴 주석을 읽는 날.",
    "경고: git push --force를 main에 실행하려 하고 있습니다. 다시 생각하세요.",
    "오늘의 당신은 어제의 당신이 계획한 내일의 당신. 코드는 여전히 어제 것.",
    "3줄의 코드가 3일간 괴롭힌 문제를 해결합니다.",
    "오늘의 부족한 요소: Stack Overflow.",
    "코드 품질은 오늘의 커피 농도에 비례합니다.",
]

LUCKY_EDITOR = {
    "zh": ["Neovim (真男人)", "VSCode (大众情人)", "Emacs (永恒之光)", "Vim (肌肉记忆)", "Notepad++ (隐藏高手)", "记事本 (混沌之王)"],
    "en": ["Neovim (enlightened)", "VSCode (safe bet)", "Emacs (eternal)", "Vim (muscle memory)", "Nano (humble)", "Notepad++ (secret master)"],
    "ja": ["Neovim (悟り)", "VSCode (安心)", "Emacs (永遠)", "Vim (筋肉記憶)", "Nano (謙虚)", "Notepad++ (隠れ高手)"],
    "ko": ["Neovim (각성)", "VSCode (안전)", "Emacs (영원)", "Vim (근육 기억)", "Nano (겸손)", "Notepad++ (숨은 고수)"],
}

LUCKY_LANG = {
    "zh": ["Python (万能胶水)", "Rust (安全到窒息)", "JavaScript (薛定谔的类型)", "Go (简洁暴力)", "Haskell (思维体操)", "C (裸奔の浪漫)"],
    "en": ["Python (glue of gods)", "Rust (safety obsession)", "JavaScript (Schrödinger's types)", "Go (brutal simplicity)", "Haskell (mental gymnastics)", "C (raw naked coding)"],
    "ja": ["Python (神の接着剤)", "Rust (安全の執着)", "JavaScript (シュレディンガーの型)", "Go (簡潔の暴力)", "Haskell (メンタル体操)", "C (全裸プログラミング)"],
    "ko": ["Python (신의 접착제)", "Rust (안전 집착)", "JavaScript (슈뢰딩거 타입)", "Go (단순 폭력)", "Haskell (멘탈 체조)", "C (누드 코딩)"],
}

WARNINGS = {
    "zh": [
        "今日切勿: rm -rf / (即使是开玩笑)",
        "今日切勿: 在不理解的代码上加 TODO",
        "今日切勿: 凌晨3点后还写代码",
        "今日切勿: 跳过测试直接 merge",
        "今日切勿: 在生产环境用 print 调试",
    ],
    "en": [
        "Do NOT: rm -rf / (even as a joke)",
        "Do NOT: add TODO to code you don't understand",
        "Do NOT: code after 3 AM",
        "Do NOT: merge without tests",
        "Do NOT: debug production with print()",
    ],
    "ja": [
        "やっちゃダメなこと: rm -rf / (冗談でも)",
        "やっちゃダメなこと: 理解していないコードに TODO",
        "やっちゃダメなこと: 午前3時以降のコーディング",
        "やっちゃダメなこと: テストなしでマージ",
        "やっちゃダメなこと: 本番環境で print デバッグ",
    ],
    "ko": [
        "절대 하지 말 것: rm -rf / (농담이라도)",
        "절대 하지 말 것: 이해 못 하는 코드에 TODO",
        "절대 하지 말 것: 새벽 3시 이후 코딩",
        "절대 하지 말 것: 테스트 없이 merge",
        "절대 하지 말 것: 프로덕션에서 print 디버깅",
    ],
}

HEADER_ART = """
   _____________________________________________
  |  _________________________________________  |
  | |  ____   _____ ____   ____               | |
  | |  |    \\ / ____|  _ \\ / ___|             | |
  | |  |  |\\ V /  __| |_) | |                 | |
  | |  |  | \\  \\ |_ |  __/| |___              | |
  | |  |__|  \\_|__|_|    \\____|              | |
  | |                                          | |
  | |     CODE FORTUNE TELLER v1.0             | |
  | |     --- 代码每日运势 ---                 | |
  | |__________________________________________| |
  |_____________________________________________|
"""

def seeded_random(seed_str: str) -> float:
    h = hashlib.sha256(seed_str.encode()).hexdigest()
    return int(h[:8], 16) / 0xFFFFFFFF


def get_fortune(lang: str, date_str: str) -> dict:
    seed = f"{lang}:{date_str}"
    pool = FORTUNES_ZH if lang == "zh" else FORTUNES_EN if lang == "en" else FORTUNES_JA if lang == "ja" else FORTUNES_KO
    r1 = seeded_random(seed + ":fortune")
    r2 = seeded_random(seed + ":editor")
    r3 = seeded_random(seed + ":lang")
    r4 = seeded_random(seed + ":warning")
    editors = LUCKY_EDITOR[lang]
    languages = LUCKY_LANG[lang]
    warnings = WARNINGS[lang]
    return {
        "fortune": pool[int(r1 * len(pool))],
        "editor": editors[int(r2 * len(editors))],
        "lucky_lang": languages[int(r3 * len(languages))],
        "warning": warnings[int(r4 * len(warnings))],
    }


def render_card(lang: str, date_str: str) -> str:
    f = get_fortune(lang, date_str)
    labels = {
        "zh": {"title": "每日代码运势", "fortune": "今日运势", "editor": "幸运编辑器", "lucky": "幸运语言", "warning": "今日禁忌", "disclaimer": "本运势由量子随机数生成，准确率与天气预报相当"},
        "en": {"title": "Daily Code Fortune", "fortune": "Today's Fortune", "editor": "Lucky Editor", "lucky": "Lucky Language", "warning": "Taboo of the Day", "disclaimer": "Generated by quantum randomness. Accuracy comparable to weather forecasts."},
        "ja": {"title": "デイリーコード占い", "fortune": "今日の運勢", "editor": "ラッキー エディタ", "lucky": "ラッキーランゲージ", "warning": "今日の禁忌", "disclaimer": "量子ランダム生成。精度は天予報と同程度。"},
        "ko": {"title": "데일리 코드 운세", "fortune": "오늘의 운세", "editor": "행운의 에디터", "lucky": "행운의 언어", "warning": "오늘의 금기", "disclaimer": "양자 랜덤으로 생성. 정확도는天气预报 수준."},
    }
    lb = labels[lang]
    card = f"""
{HEADER_ART}

  Date: {date_str}
  {lb['title']}
{'='*50}

  > {lb['fortune']}:
    {f['fortune']}

  > {lb['editor']}:
    {f['editor']}

  > {lb['lucky']}:
    {f['lucky_lang']}

  > {lb['warning']}:
    {f['warning']}

{'='*50}
  * {lb['disclaimer']}
  * Powered by CTest Quantum Fortune Engine (TM)
    A project by @Picodesu
"""
    return card


def main():
    langs = ["zh", "en", "ja", "ko"]
    today = datetime.now().strftime("%Y-%m-%d")
    if len(sys.argv) > 1 and sys.argv[1] == "--lang":
        if len(sys.argv) > 2 and sys.argv[2] == "all":
            for lang in langs:
                print(render_card(lang, today))
        elif len(sys.argv) > 2 and sys.argv[2] in langs:
            print(render_card(sys.argv[2], today))
        else:
            print("Usage: python fortune.py [--lang zh|en|ja|ko|all]")
            sys.exit(1)
    else:
        for lang in langs:
            print(render_card(lang, today))


if __name__ == "__main__":
    main()
