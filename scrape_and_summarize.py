import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

url = "https://seneca.center/"

async def fetch_content(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        content = await page.content()
        title = await page.title()
        await browser.close()
        return content, title

def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")
    # Remove scripts, styles, nav, footer, and aside
    for tag in soup(["script", "style", "nav", "footer", "aside"]):
        tag.decompose()
    text = soup.get_text(separator="\n", strip=True)
    return text

def summarize(text, title, sentences_count=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, sentences_count=sentences_count)
    print(f"Summary of: {title}\n")
    for sentence in summary:
        print("-", sentence)

if __name__ == "__main__":
    html, title = asyncio.run(fetch_content(url))
    text = extract_text(html)
    summarize(text, title) 