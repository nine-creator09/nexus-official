#!/bin/bash
# NEXUS AI News - 自動更新スクリプト
cd /Users/blackwood/Desktop/NEXUS_Production/website
/usr/bin/python3 ai_news.py >> ai_news_cron.log 2>&1
echo "--- $(date '+%Y-%m-%d %H:%M:%S JST') 完了 ---" >> ai_news_cron.log
