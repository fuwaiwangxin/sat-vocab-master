#!/usr/bin/env python3
"""
P5: Programmatic SEO - Generate individual HTML pages for each SAT word.
Each page is a standalone, SEO-optimized page that:
1. Shows the word definition, image, and music connection
2. Has proper meta tags for Google indexing
3. Links back to the main app
4. URL format: /word/aberration.html

Run: python3 generate_seo_pages.py
"""

import json
import os
import html

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VOCAB_FILE = os.path.join(BASE_DIR, 'vocab_data.json')
VISUAL_FILE = os.path.join(BASE_DIR, 'visual_data.json')
MUSIC_FILE = os.path.join(BASE_DIR, 'music_data.json')
WORD_DIR = os.path.join(BASE_DIR, 'word')

# Load data
with open(VOCAB_FILE, 'r', encoding='utf-8') as f:
    vocab = json.load(f)

visual = {}
if os.path.exists(VISUAL_FILE):
    with open(VISUAL_FILE, 'r', encoding='utf-8') as f:
        visual = json.load(f)

music = {}
if os.path.exists(MUSIC_FILE):
    with open(MUSIC_FILE, 'r', encoding='utf-8') as f:
        music = json.load(f)

# Create word directory
os.makedirs(WORD_DIR, exist_ok=True)

def safe_filename(word):
    import re
    name = word.lower()
    name = re.sub(r'[\/\\:*?"<>|\'\s]+', '_', name)
    name = re.sub(r'_+', '_', name)
    name = name.strip('_')
    return name

def generate_word_page(w):
    word = w['word']
    wl = word.lower()
    pronunciation = html.escape(w.get('pronunciation', ''))
    definition = html.escape(w.get('engDef', ''))
    extra = html.escape(w.get('extra', ''))

    # Visual data
    vis = visual.get(wl, {})
    visual_desc = html.escape(vis.get('visual', ''))
    sentence = html.escape(vis.get('sentence', f'The word {word} is commonly used in academic contexts.'))
    emoji_scene = vis.get('emoji_scene', '📝')

    # Music data
    mus = music.get(wl, {})
    music_song = html.escape(mus.get('song', ''))
    music_artist = html.escape(mus.get('artist', ''))
    music_connection = html.escape(mus.get('connection', ''))

    # Image
    fn = safe_filename(wl)
    img_path = f'../images/{fn}.jpg'

    # Music section HTML
    music_html = ''
    if music_song:
        music_html = f'''
    <div class="music-box">
      <h3>🎵 Music Connection</h3>
      <p><strong>"{music_song}"</strong> by {music_artist}</p>
      <p class="music-desc">{music_connection}</p>
    </div>'''

    # Visual section HTML
    visual_html = ''
    if visual_desc:
        visual_html = f'''
    <div class="visual-box">
      <h3>🖼️ Picture This</h3>
      <p><em>{visual_desc}</em></p>
    </div>'''

    page_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{word} - SAT Vocabulary Definition with AI Image &amp; Music | SAT Vocab Master</title>
<meta name="description" content="Learn the SAT word '{word}' {pronunciation}: {definition[:150]}. Study with AI-generated images, music connections, and interactive flashcards.">
<meta name="keywords" content="{word}, SAT vocabulary, {word} definition, {word} meaning, SAT word {word}, SAT prep">
<meta property="og:title" content="{word} - SAT Vocabulary with AI Image &amp; Music">
<meta property="og:description" content="{definition[:200]}">
<meta property="og:image" content="https://fun2learnsatvocabtw.com/images/{fn}.jpg">
<meta property="og:url" content="https://fun2learnsatvocabtw.com/word/{fn}.html">
<meta property="og:type" content="article">
<link rel="canonical" href="https://fun2learnsatvocabtw.com/word/{fn}.html">
<meta name="robots" content="index, follow">
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-LCGNFJ3J9R"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-LCGNFJ3J9R');</script>
<!-- Structured Data for Google -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "DefinedTerm",
  "name": "{word}",
  "description": "{definition[:300]}",
  "inDefinedTermSet": {{
    "@type": "DefinedTermSet",
    "name": "SAT Vocabulary"
  }}
}}
</script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI',system-ui,-apple-system,sans-serif;background:#0F0F1A;color:#E8E8F0;min-height:100vh;display:flex;flex-direction:column}}
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
.img-wrap{{border-radius:10px;overflow:hidden;margin:16px 0}}
.img-wrap img{{width:100%;display:block;border-radius:10px;max-height:400px;object-fit:cover}}
.sentence{{font-style:italic;background:#16213E;padding:14px;border-radius:8px;line-height:1.5;border-left:3px solid #A29BFE}}
.music-box{{background:rgba(233,30,99,.08);border-left:3px solid #E91E63;padding:14px;border-radius:0 8px 8px 0}}
.music-box h3{{color:#E91E63}}
.music-desc{{color:#8888AA;font-size:.9em;margin-top:4px}}
.visual-box{{background:rgba(108,92,231,.08);border-left:3px solid #A29BFE;padding:14px;border-radius:0 8px 8px 0}}
.cta{{text-align:center;padding:30px;margin-top:20px}}
.cta-btn{{display:inline-flex;align-items:center;gap:8px;padding:14px 36px;border-radius:30px;background:linear-gradient(135deg,#00B894,#55EFC4);color:#fff;text-decoration:none;font-size:1.1em;font-weight:700;transition:.2s;box-shadow:0 4px 20px rgba(0,184,148,.3)}}
.cta-btn:hover{{transform:translateY(-3px);box-shadow:0 8px 30px rgba(0,184,148,.4)}}
.related{{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}}
.related a{{padding:6px 14px;border-radius:20px;background:rgba(108,92,231,.12);color:#A29BFE;text-decoration:none;font-size:.85em;border:1px solid rgba(108,92,231,.25);transition:.2s}}
.related a:hover{{background:rgba(108,92,231,.25)}}
footer{{text-align:center;padding:20px;color:#8888AA;font-size:.8em;border-top:1px solid #333355;margin-top:auto}}
@media(max-width:600px){{h1{{font-size:1.8em}}.container{{padding:20px 16px}}}}
</style>
</head>
<body>
<div class="container">
  <a class="back" href="../">← Back to SAT Vocab Master</a>

  <div class="word-header">
    <div class="emoji">{emoji_scene}</div>
    <h1>{word}</h1>
    <div class="pron">{pronunciation}</div>
    <button class="speak-btn" onclick="speak(this.dataset.w)" data-w="{word}">🔊 Listen</button>
  </div>

  <div class="card">
    <h3>📖 Definition</h3>
    <p>{definition}</p>
  </div>

  <div class="img-wrap">
    <img src="{img_path}" alt="AI-generated image for SAT word {word}"
         onerror="this.style.display='none'">
  </div>

  {visual_html}

  <div class="card">
    <h3>💬 Example Sentence</h3>
    <div class="sentence">{sentence}</div>
  </div>

  {music_html}

  EXTRA_PLACEHOLDER

  <div class="cta">
    <a class="cta-btn" href="../">🏆 Learn All 2000+ SAT Words Free</a>
    <div class="related" id="relatedWords"></div>
  </div>
</div>

<footer>
  <p>&copy; 2026 <a href="../" style="color:#A29BFE">SAT Vocab Master</a> | fun2learnsatvocabtw.com</p>
  <p style="margin-top:4px">Master SAT vocabulary with AI-powered images, music connections &amp; interactive quizzes</p>
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
</html>'''

    # Replace extra placeholder
    extra_html = f"<div class='card'><h3>📝 Word Roots &amp; Related</h3><p>{extra}</p></div>" if extra else ""
    page_html = page_html.replace('EXTRA_PLACEHOLDER', extra_html)

    # Write the file
    filepath = os.path.join(WORD_DIR, f'{fn}.html')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(page_html)
    return filepath

# Generate sitemap
def generate_sitemap(words):
    sitemap_path = os.path.join(BASE_DIR, 'sitemap.xml')
    urls = ['  <url><loc>https://fun2learnsatvocabtw.com/</loc><priority>1.0</priority><changefreq>weekly</changefreq></url>']
    for w in words:
        fn = safe_filename(w['word'].lower())
        urls.append(f'  <url><loc>https://fun2learnsatvocabtw.com/word/{fn}.html</loc><priority>0.7</priority><changefreq>monthly</changefreq></url>')

    sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>'''

    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(sitemap)
    print(f'Sitemap generated: {sitemap_path} ({len(urls)} URLs)')

# Generate robots.txt
def generate_robots():
    robots_path = os.path.join(BASE_DIR, 'robots.txt')
    robots = '''User-agent: *
Allow: /
Sitemap: https://fun2learnsatvocabtw.com/sitemap.xml
'''
    with open(robots_path, 'w', encoding='utf-8') as f:
        f.write(robots)
    print(f'robots.txt generated: {robots_path}')

# Main
if __name__ == '__main__':
    print(f'Generating SEO pages for {len(vocab)} words...')
    count = 0
    for w in vocab:
        generate_word_page(w)
        count += 1
        if count % 200 == 0:
            print(f'  ...{count}/{len(vocab)} pages generated')

    print(f'All {count} word pages generated in {WORD_DIR}/')

    generate_sitemap(vocab)
    generate_robots()

    print('\nDone! Next steps:')
    print('1. git add word/ sitemap.xml robots.txt')
    print('2. git commit -m "Add programmatic SEO pages for all SAT words"')
    print('3. git push')
    print(f'\nEach word now has its own Google-indexable page at:')
    print(f'  https://fun2learnsatvocabtw.com/word/aberration.html')
