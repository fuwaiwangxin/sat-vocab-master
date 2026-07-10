#!/usr/bin/env python3
"""Batch-translate SAT vocab definitions to Chinese via DeepSeek API.

Reads vocab_data.json, adds a `zh` field to each entry.
Idempotent: skips entries that already have `zh`.
Saves progress every SAVE_EVERY words so a kill/crash never loses more than that.

Usage:
    export DEEPSEEK_API_KEY=sk-...
    python3 translate_to_zh.py

Optional env vars:
    DEEPSEEK_MODEL     (default: deepseek-chat)
    DEEPSEEK_BASE_URL  (default: https://api.deepseek.com/v1)
    WORKERS            (default: 20)
    SAVE_EVERY         (default: 50)
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

VOCAB_PATH = Path(__file__).parent / "vocab_data.json"

API_KEY = os.environ.get("DEEPSEEK_API_KEY")
MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
BASE_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
WORKERS = int(os.environ.get("WORKERS", "20"))
SAVE_EVERY = int(os.environ.get("SAVE_EVERY", "50"))

if not API_KEY:
    sys.exit("ERROR: export DEEPSEEK_API_KEY=sk-... first")

SYSTEM_PROMPT = (
    "You are an expert SAT vocabulary translator for Chinese high-school students.\n"
    "Given an English SAT vocab word and its English definition, produce a concise Chinese translation.\n"
    "\n"
    "Rules:\n"
    "- Preserve the part-of-speech tag (v./n./adj./adv./prep. etc.) at the start.\n"
    "- Preserve multi-sense numbering exactly (1)/2)/3) etc.).\n"
    "- Use Chinese punctuation (，、；（）).\n"
    "- Keep it tight and natural, like a Chinese SAT prep book.\n"
    "- If a sense references a phrasal form (e.g. `abide by`), keep the English phrase in parentheses.\n"
    "- Return ONLY the Chinese translation. No extra commentary, no code fences, no labels."
)


def translate(word: str, eng_def: str) -> str:
    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Word: {word}\nDefinition: {eng_def}"},
        ],
        "temperature": 0.3,
        "max_tokens": 300,
    }
    req = urllib.request.Request(
        f"{BASE_URL}/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
    )
    last_err = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                payload = json.loads(resp.read())
                text = payload["choices"][0]["message"]["content"].strip()
                # Strip common LLM residue
                if text.startswith("```"):
                    text = text.strip("`").strip()
                    if text.lower().startswith(("chinese", "translation", "zh")):
                        text = text.split("\n", 1)[-1].strip()
                return text
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError) as e:
            last_err = e
            if attempt < 3:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"failed after 4 attempts: {last_err}")


def main() -> None:
    with VOCAB_PATH.open() as f:
        vocab = json.load(f)

    pending = [(i, w) for i, w in enumerate(vocab) if not w.get("zh")]
    print(
        f"Total: {len(vocab)} | Already translated: {len(vocab) - len(pending)} | "
        f"Pending: {len(pending)} | Workers: {WORKERS} | Model: {MODEL}"
    )
    if not pending:
        print("Nothing to do.")
        return

    def save() -> None:
        with VOCAB_PATH.open("w") as f:
            json.dump(vocab, f, ensure_ascii=False)

    def worker(idx_word):
        i, w = idx_word
        try:
            return i, translate(w["word"], w["engDef"]), None
        except Exception as e:
            return i, None, str(e)

    done = 0
    errors: list[tuple[int, str]] = []
    start = time.time()
    samples_shown = 0

    try:
        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            futures = [pool.submit(worker, iw) for iw in pending]
            for fut in as_completed(futures):
                i, zh, err = fut.result()
                if err:
                    errors.append((i, err))
                    print(f"  [ERR] id={vocab[i]['id']} word={vocab[i]['word']!r}: {err[:120]}")
                else:
                    vocab[i]["zh"] = zh
                    if samples_shown < 5:
                        print(f"  [SAMPLE] {vocab[i]['word']} → {zh[:80]}")
                        samples_shown += 1
                done += 1
                if done % SAVE_EVERY == 0:
                    save()
                    elapsed = time.time() - start
                    rate = done / elapsed if elapsed else 0
                    eta_min = (len(pending) - done) / rate / 60 if rate else 0
                    print(
                        f"  Progress: {done}/{len(pending)} "
                        f"({done / len(pending) * 100:.1f}%) "
                        f"rate={rate:.1f}/s eta={eta_min:.1f}min"
                    )
    except KeyboardInterrupt:
        print("\nInterrupted — saving partial results before exit.")
    finally:
        save()

    ok = done - len(errors)
    print(f"\nDone. Success: {ok} | Errors: {len(errors)} | Elapsed: {(time.time() - start) / 60:.1f} min")
    if errors:
        print("First 5 errors:")
        for i, e in errors[:5]:
            print(f"  id={vocab[i]['id']} word={vocab[i]['word']!r}: {e[:200]}")
        print("Re-run to retry only the failures (script is idempotent).")


if __name__ == "__main__":
    main()
