#!/usr/bin/env python3
"""Dry-run: translate 5 diverse sample SAT words to Chinese to eyeball quality.

Does NOT touch vocab_data.json. Just prints results.

Usage:
    export DEEPSEEK_API_KEY=sk-...
    python3 dry_run_translate.py
"""

import json
from pathlib import Path

from translate_to_zh import translate

SAMPLES = ["abide", "acoustic", "acclaim", "quaint", "usurp"]

with (Path(__file__).parent / "vocab_data.json").open() as f:
    vocab = json.load(f)
by_word = {w["word"]: w for w in vocab}

print(f"Translating {len(SAMPLES)} samples...\n")
for word in SAMPLES:
    w = by_word[word]
    print(f"── {word} ── {w['engDef']}")
    try:
        zh = translate(word, w["engDef"])
        print(f"   → {zh}\n")
    except Exception as e:
        print(f"   [ERROR] {e}\n")
