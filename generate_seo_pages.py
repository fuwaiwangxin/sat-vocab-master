#!/usr/bin/env python3
"""Programmatic SEO pages for 中国版 SAT词汇大师.

Each page:
- Bilingual title/description targeting Baidu queries like "abide 什么意思"
- Chinese meaning (from zh field) rendered ABOVE English definition
- Baidu Analytics (site ID from BAIDU_SITE_ID env; TODO placeholder otherwise)
- No music section (removed in china-edition)
- Canonical URL from CHINA_DOMAIN env (TODO placeholder otherwise)

Run:
    CHINA_DOMAIN=example.cn BAIDU_SITE_ID=abc123 python3 generate_seo_pages.py
"""

import html
import json
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VOCAB_FILE = os.path.join(BASE_DIR, "vocab_data.json")
VISUAL_FILE = os.path.join(BASE_DIR, "visual_data.json")
WORD_DIR = os.path.join(BASE_DIR, "word")

DOMAIN = os.environ.get("CHINA_DOMAIN", "TODO_CHINA_DOMAIN.com")
BAIDU_SITE_ID = os.environ.get("BAIDU_SITE_ID", "f791641966b50e0bfda57b90b7e896ad")

with open(VOCAB_FILE, encoding="utf-8") as f:
    vocab = json.load(f)

visual = {}
if os.path.exists(VISUAL_FILE):
    with open(VISUAL_FILE, encoding="utf-8") as f:
        visual = json.load(f)

os.makedirs(WORD_DIR, exist_ok=True)


def safe_filename(word):
    name = word.lower()
    name = re.sub(r'[\/\\:*?"<>|\'\s]+', "_", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_")


def generate_word_page(w):
    word = w["word"]
    wl = word.lower()
    pronunciation = html.escape(w.get("pronunciation", ""))
    definition = html.escape(w.get("engDef", ""))
    zh = html.escape(w.get("zh", ""))
    extra = html.escape(w.get("extra", ""))

    vis = visual.get(wl, {})
    visual_desc = html.escape(vis.get("visual", ""))
    sentence = html.escape(
        vis.get("sentence", f"The word {word} is commonly used in academic contexts.")
    )
    emoji_scene = vis.get("emoji_scene", "📝")

    fn = safe_filename(wl)
    img_path = f"../images/{fn}.jpg"

    # Descriptor for meta description: prefer zh if we have it, fall back to engDef.
    meta_desc = zh[:160] if zh else definition[:160]

    visual_html = (
        f"""
    <div class="visual-box">
      <h3>🖼️ 图像联想</h3>
      <p><em>{visual_desc}</em></p>
    </div>"""
        if visual_desc
        else ""
    )

    extra_html = (
        f"""<div class="card"><h3>📝 词根 &amp; 相关</h3><p>{extra}</p></div>"""
        if extra
        else ""
    )

    zh_html = f'<p class="zh">{zh}</p>' if zh else ""

    page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{word} 是什么意思？— SAT 词汇释义 | SAT词汇大师</title>
<meta name="description" content="SAT 单词 {word} {pronunciation} 的中文意思：{meta_desc}。附例句、AI 配图、发音。">
<meta name="keywords" content="{word},{word} 什么意思,{word} 中文,{word} 释义,SAT词汇,SAT单词,SAT备考">
<meta property="og:title" content="{word} 是什么意思？— SAT 词汇释义">
<meta property="og:description" content="{meta_desc}">
<meta property="og:image" content="https://{DOMAIN}/images/{fn}.jpg">
<meta property="og:url" content="https://{DOMAIN}/word/{fn}.html">
<meta property="og:type" content="article">
<link rel="canonical" href="https://{DOMAIN}/word/{fn}.html">
<meta name="robots" content="index, follow">
<!-- 百度统计 -->
<script>var _hmt=_hmt||[];(function(){{var hm=document.createElement("script");hm.src="https://hm.baidu.com/hm.js?{BAIDU_SITE_ID}";var s=document.getElementsByTagName("script")[0];s.parentNode.insertBefore(hm,s);}})();</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"DefinedTerm","name":"{word}","description":"{meta_desc}","inDefinedTermSet":{{"@type":"DefinedTermSet","name":"SAT Vocabulary"}}}}
</script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'PingFang SC','Helvetica Neue','Segoe UI',system-ui,sans-serif;background:#0F0F1A;color:#E8E8F0;min-height:100vh;display:flex;flex-direction:column}}
.container{{max-width:700px;margin:0 auto;padding:30px 20px;flex:1}}
.back{{display:inline-flex;align-items:center;gap:6px;color:#A29BFE;text-decoration:none;font-size:.9em;margin-bottom:24px;padding:8px 16px;border-radius:20px;background:rgba(108,92,231,.1);transition:.2s}}
.back:hover{{background:rgba(108,92,231,.2)}}
.word-header{{text-align:center;margin-bottom:28px}}
.emoji{{font-size:3em;margin-bottom:8px}}
h1{{font-size:2.4em;font-weight:800;background:linear-gradient(135deg,#6C5CE7,#A29BFE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:6px}}
.pron{{color:#8888AA;font-size:1.1em}}
.speak-btn{{display:inline-flex;align-items:center;gap:6px;padding:8px 20px;border-radius:20px;background:linear-gradient(135deg,#6C5CE7,#A29BFE);color:#fff;border:none;cursor:pointer;font-size:.9em;margin-top:12px;transition:.2s}}
.speak-btn:hover{{transform:translateY(-2px)}}
.card{{background:#1E1E32;border:1px solid #333355;border-radius:12px;padding:22px;margin-bottom:16px}}
.card h3{{color:#A29BFE;margin-bottom:10px;font-size:1em}}
.card p,.card li{{line-height:1.6;font-size:.95em}}
.zh{{color:#A29BFE;font-size:1.1em;font-weight:600;margin-bottom:10px;line-height:1.5}}
.eng-def{{color:#B0B0C0;font-size:.9em;line-height:1.6}}
.img-wrap{{border-radius:10px;overflow:hidden;margin:16px 0}}
.img-wrap img{{width:100%;display:block;border-radius:10px;max-height:400px;object-fit:cover}}
.sentence{{font-style:italic;background:#16213E;padding:14px;border-radius:8px;line-height:1.5;border-left:3px solid #A29BFE}}
.visual-box{{background:rgba(108,92,231,.08);border-left:3px solid #A29BFE;padding:14px;border-radius:0 8px 8px 0}}
.cta{{text-align:center;padding:30px;margin-top:20px}}
.cta-btn{{display:inline-flex;align-items:center;gap:8px;padding:14px 36px;border-radius:30px;background:linear-gradient(135deg,#00B894,#55EFC4);color:#fff;text-decoration:none;font-size:1.1em;font-weight:700;transition:.2s;box-shadow:0 4px 20px rgba(0,184,148,.3)}}
.cta-btn:hover{{transform:translateY(-3px);box-shadow:0 8px 30px rgba(0,184,148,.4)}}
footer{{text-align:center;padding:20px;color:#8888AA;font-size:.8em;border-top:1px solid #333355;margin-top:auto}}
@media(max-width:600px){{h1{{font-size:1.8em}}.container{{padding:20px 16px}}}}
</style>
</head>
<body>
<div class="container">
  <a class="back" href="../">← 返回 SAT词汇大师</a>

  <div class="word-header">
    <div class="emoji">{emoji_scene}</div>
    <h1>{word}</h1>
    <div class="pron">{pronunciation}</div>
    <button class="speak-btn" onclick="speak(this.dataset.w)" data-w="{word}">🔊 听发音</button>
  </div>

  <div class="card">
    <h3>📖 释义</h3>
    {zh_html}
    <p class="eng-def">{definition}</p>
  </div>

  <div class="img-wrap">
    <img src="{img_path}" alt="SAT 单词 {word} 的 AI 配图" onerror="this.style.display='none'">
  </div>

  {visual_html}

  <div class="card">
    <h3>💬 例句</h3>
    <div class="sentence">{sentence}</div>
  </div>

  {extra_html}

  <div class="cta">
    <a class="cta-btn" href="../">🏆 免费学 2000+ SAT 单词</a>
  </div>
</div>

<footer>
  <p>&copy; 2026 <a href="../" style="color:#A29BFE">SAT词汇大师</a></p>
  <p style="margin-top:4px">AI 配图 + 互动测试，助你搞定 SAT 词汇</p>
</footer>

<script>
function speak(word){{
  if(!('speechSynthesis' in window))return;
  speechSynthesis.cancel();
  var u=new SpeechSynthesisUtterance(word);
  u.lang='en-US';u.rate=0.75;u.pitch=1.0;u.volume=1.0;
  var vs=speechSynthesis.getVoices();
  var voice=vs.find(function(v){{return v.lang==='en-US'}});
  if(voice)u.voice=voice;
  speechSynthesis.speak(u);
}}
if('speechSynthesis' in window){{speechSynthesis.getVoices();speechSynthesis.onvoiceschanged=function(){{speechSynthesis.getVoices()}}}}
</script>
</body>
</html>"""

    filepath = os.path.join(WORD_DIR, f"{fn}.html")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(page)


def generate_sitemap(words):
    sitemap_path = os.path.join(BASE_DIR, "sitemap.xml")
    urls = [
        f'  <url><loc>https://{DOMAIN}/</loc><priority>1.0</priority><changefreq>weekly</changefreq></url>'
    ]
    for w in words:
        fn = safe_filename(w["word"].lower())
        urls.append(
            f'  <url><loc>https://{DOMAIN}/word/{fn}.html</loc><priority>0.7</priority><changefreq>monthly</changefreq></url>'
        )
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>"""
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"Sitemap: {len(urls)} URLs")


def generate_robots():
    robots_path = os.path.join(BASE_DIR, "robots.txt")
    with open(robots_path, "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: https://{DOMAIN}/sitemap.xml\n")
    print("robots.txt updated")


if __name__ == "__main__":
    print(
        f"Generating {len(vocab)} SEO pages "
        f"(DOMAIN={DOMAIN}, BAIDU_SITE_ID={BAIDU_SITE_ID})"
    )
    for i, w in enumerate(vocab, 1):
        generate_word_page(w)
        if i % 500 == 0:
            print(f"  {i}/{len(vocab)}")
    print(f"Done: {len(vocab)} pages in {WORD_DIR}/")
    generate_sitemap(vocab)
    generate_robots()
