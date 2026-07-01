import re

with open(r"C:\Users\MSI\.gemini\antigravity-ide\brain\3ea05337-822d-4b69-ad77-865f2831cd41\.system_generated\steps\5\content.md", 'r', encoding='utf-8') as f:
    content = f.read()

# Extract bio
bio_match = re.search(r'<meta name="description" content="(.*?)">', content)
if bio_match:
    print("Bio:", bio_match.group(1))

# Extract title
title_match = re.search(r'<title>(.*?)</title>', content)
if title_match:
    print("Title:", title_match.group(1))

# Extract repositories
# GitHub repos are usually in a span with class "repo" or itemprop="name codeRepository"
repos = re.findall(r'<span class="repo" title="(.*?)">', content)
if repos:
    print("Repos:", set(repos))

repos_alt = re.findall(r'itemprop="name codeRepository"[^>]*>\s*(.*?)\s*</a>', content)
if repos_alt:
    print("Repos (alt):", set(repos_alt))
    
# languages
languages = re.findall(r'<span itemprop="programmingLanguage">(.*?)</span>', content)
if languages:
    print("Languages:", set(languages))
