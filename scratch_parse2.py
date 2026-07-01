import re
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.in_repo = False
        self.in_org = False
        
    def handle_data(self, data):
        if data.strip():
            self.text.append(data.strip())

with open(r"C:\Users\MSI\.gemini\antigravity-ide\brain\3ea05337-822d-4b69-ad77-865f2831cd41\.system_generated\steps\5\content.md", 'r', encoding='utf-8') as f:
    content = f.read()

parser = MyHTMLParser()
parser.feed(content)

with open(r"d:\medical-rag-bot\scratch_text.txt", "w", encoding='utf-8') as f:
    for t in parser.text:
        f.write(t + "\n")
