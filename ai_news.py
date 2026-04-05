#!/usr/bin/env python3
"""
NEXUS AI News Aggregator
━━━━━━━━━━━━━━━━━━━━━━━
全世界15ソースからAI関連ニュースを取得し、JSONファイルに出力。
ai_news_dashboard.html がこのJSONを読み込んで表示する。

使い方:
  python3 ai_news.py              → JSONファイルに出力
  python3 ai_news.py --print      → ターミナルにも表示
"""

import feedparser
import json
import re
import sys
import hashlib
from base64 import b64encode
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ━━━ Output ━━━
OUTPUT_FILE = Path(__file__).parent / "ai_news_data.json"

# ━━━ ニュースソース（15ソース） ━━━
FEEDS = [
    {"name": "The Verge",       "key": "verge",         "flag": "🇺🇸", "cls": "src-verge",         "lang": "en", "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"},
    {"name": "TechCrunch",      "key": "techcrunch",    "flag": "🇺🇸", "cls": "src-techcrunch",    "lang": "en", "url": "https://techcrunch.com/category/artificial-intelligence/feed/"},
    {"name": "MIT Tech Review", "key": "mit",           "flag": "🇺🇸", "cls": "src-mit",           "lang": "en", "url": "https://www.technologyreview.com/feed/"},
    {"name": "Ars Technica",    "key": "ars",           "flag": "🇺🇸", "cls": "src-ars",           "lang": "en", "url": "https://feeds.arstechnica.com/arstechnica/features"},
    {"name": "VentureBeat",     "key": "venturebeat",   "flag": "🇺🇸", "cls": "src-venturebeat",   "lang": "en", "url": "https://venturebeat.com/category/ai/feed/"},
    {"name": "Wired",           "key": "wired",         "flag": "🇺🇸", "cls": "src-wired",         "lang": "en", "url": "https://www.wired.com/feed/tag/ai/latest/rss"},
    {"name": "ITmedia AI+",     "key": "itmedia",       "flag": "🇯🇵", "cls": "src-itmedia",       "lang": "ja", "url": "https://rss.itmedia.co.jp/rss/2.0/aiplus.xml"},
    {"name": "BBC Technology",  "key": "bbc",           "flag": "🇬🇧", "cls": "src-bbc",           "lang": "en", "url": "http://feeds.bbci.co.uk/news/technology/rss.xml"},
    {"name": "The Guardian AI", "key": "guardian",      "flag": "🇬🇧", "cls": "src-guardian",      "lang": "en", "url": "https://www.theguardian.com/technology/artificialintelligenceai/rss"},
    {"name": "France24 Tech",   "key": "france24",      "flag": "🇫🇷", "cls": "src-france24",      "lang": "en", "url": "https://news.google.com/rss/search?q=site:france24.com+AI+artificial+intelligence&hl=en"},
    {"name": "DW Tech",         "key": "dw",            "flag": "🇩🇪", "cls": "src-dw",            "lang": "en", "url": "https://news.google.com/rss/search?q=site:dw.com+AI+artificial+intelligence&hl=en"},
    {"name": "Korea Herald Tech","key": "koreaherald",  "flag": "🇰🇷", "cls": "src-koreaherald",   "lang": "en", "url": "https://news.google.com/rss/search?q=site:koreaherald.com+AI+artificial+intelligence&hl=en"},
    {"name": "SCMP",            "key": "scmp",          "flag": "🇨🇳", "cls": "src-scmp",          "lang": "en", "url": "https://news.google.com/rss/search?q=site:scmp.com+AI+artificial+intelligence&hl=en"},
    {"name": "Reuters",         "key": "reuters",       "flag": "🌐", "cls": "src-reuters",        "lang": "en", "url": "https://news.google.com/rss/search?q=site:reuters.com+artificial+intelligence&hl=en"},
    {"name": "Economic Times",  "key": "economictimes", "flag": "🇮🇳", "cls": "src-economictimes", "lang": "en", "url": "https://economictimes.indiatimes.com/tech/rssfeeds/13357305.cms"},
]

# ━━━ AIキーワード ━━━
AI_RE = re.compile(
    r'\b(AI|artificial.?intelligence|GPT|LLM|machine.?learning|deep.?learning|'
    r'neural|chatbot|OpenAI|Anthropic|gemini|claude|roboti|autonomous|'
    r'人工知能|生成AI|AIモデル|大規模言語)\b', re.IGNORECASE
)

def make_id(title):
    return b64encode(hashlib.md5(title.encode()).digest()).decode().rstrip('=')[:12]

def parse_date(entry):
    for attr in ['published_parsed', 'updated_parsed']:
        t = getattr(entry, attr, None)
        if t:
            try:
                return datetime(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec, tzinfo=timezone.utc)
            except Exception:
                pass
    return datetime.now(timezone.utc)

def fetch_all(hours=168):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    articles = []
    results = {}

    for feed_info in FEEDS:
        key = feed_info["key"]
        try:
            print(f"  📡 {feed_info['name']}...", end=" ", flush=True)
            feed = feedparser.parse(feed_info["url"])
            count = 0
            for entry in feed.entries[:30]:
                title = (entry.get('title') or '').strip()
                summary = re.sub(r'<[^>]+>', '', entry.get('summary', ''))[:200].strip()
                link = (entry.get('link') or '').strip()
                pub_date = parse_date(entry)

                if pub_date >= cutoff and AI_RE.search(f"{title} {summary}"):
                    articles.append({
                        "id": make_id(title),
                        "title": title,
                        "summary": summary,
                        "link": link,
                        "date": pub_date.isoformat(),
                        "source": feed_info["name"],
                        "key": key,
                        "cls": feed_info["cls"],
                        "flag": feed_info["flag"],
                        "articleLang": feed_info["lang"],
                    })
                    count += 1
            results[key] = {"status": "ok", "count": count}
            print(f"✅ {count}件")
        except Exception as e:
            results[key] = {"status": "fail", "count": 0}
            print(f"❌ {e}")

    # 重複除去 & ソート
    seen = set()
    unique = []
    for a in sorted(articles, key=lambda x: x['date'], reverse=True):
        short = a['title'][:50].lower()
        if short not in seen:
            seen.add(short)
            unique.append(a)

    return unique, results

def main():
    jst = timezone(timedelta(hours=9))
    now = datetime.now(jst)
    print()
    print("━" * 50)
    print(f"  NEXUS AI News Aggregator")
    print(f"  {now.strftime('%Y-%m-%d %H:%M')} JST")
    print(f"  15ソースから直近1週間のAIニュースを取得")
    print("━" * 50)
    print()

    articles, results = fetch_all(hours=168)

    # JSON出力
    data = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "articleCount": len(articles),
        "sourceResults": results,
        "articles": articles,
    }
    OUTPUT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

    ok = sum(1 for r in results.values() if r['status'] == 'ok')
    fail = sum(1 for r in results.values() if r['status'] == 'fail')

    print()
    print("━" * 50)
    print(f"  ✅ {len(articles)}記事を取得")
    print(f"  📡 ソース: {ok}成功 / {fail}失敗")
    print(f"  💾 {OUTPUT_FILE.name} に保存完了")
    print("━" * 50)

    if "--print" in sys.argv:
        print()
        for i, a in enumerate(articles[:20], 1):
            print(f"  [{i:02d}] {a['flag']} {a['title'][:70]}")
            print(f"       {a['source']} | {a['date'][:16]}")
            print()

if __name__ == "__main__":
    main()
