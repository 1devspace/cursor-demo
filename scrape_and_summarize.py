import os
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import httpx

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
    for tag in soup(["script", "style", "nav", "footer", "aside"]):
        tag.decompose()
    text = soup.get_text(separator="\n", strip=True)
    return text

def summarize_with_grok(text, title):
    api_key = os.getenv("GROK_API_KEY")
    if not api_key:
        raise ValueError("GROK_API_KEY environment variable not set.")
    prompt = f"""
You are an expert summarizer. Summarize the following website content in a concise, clear way. Add additional notes and insights that would be helpful for someone interested in the site.\n\nTitle: {title}\n\nContent:\n{text}\n\nSummary with additional notes and content:
"""
    url = "https://api.grok.x.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "grok-1",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
        "temperature": 0.7
    }
    response = httpx.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    result = response.json()
    print(f"Summary of: {title}\n")
    print(result["choices"][0]["message"]["content"].strip())

if __name__ == "__main__":
    html, title = asyncio.run(fetch_content(url))
    text = extract_text(html)
    summarize_with_grok(text, title) 