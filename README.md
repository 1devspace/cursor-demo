# cursor-demo

A simple Python script to scrape a website's content and summarize it using an LLM API (supports xAI Grok, Anthropic Claude, or OpenAI GPT).

## Features
- Scrapes and extracts main content from any website (including JavaScript-rendered content)
- Summarizes the content using an LLM API
- Supports xAI Grok, Anthropic Claude, or OpenAI GPT (with minor code changes)

## Requirements
- Python 3.9+
- [Playwright](https://playwright.dev/python/) (for headless browser scraping)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
- [httpx](https://www.python-httpx.org/)
- LLM API package (e.g., `anthropic`, `openai`) if using those providers

Install dependencies:
```bash
pip install -r requirements.txt
python3 -m playwright install
```

## Usage

### 2. Run the script
```bash
python3 scrape_and_summarize.py
```

The script will scrape the hardcoded URL (currently `https://seneca.center/`), extract the main content, and print a summary using your chosen LLM provider.

## Customization
- To change the website, edit the `url` variable in `scrape_and_summarize.py`.
- To switch LLM providers, update the summarization function and environment variable as shown in the code and above.

## License
MIT 