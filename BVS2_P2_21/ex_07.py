import json
import sys
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

GEMINI_API_KEY = ""
genai.configure(api_key=GEMINI_API_KEY)

def fetch_wikipedia(title):
    url = f"https://en.wikipedia.org/api/rest_v1/page/html/{title}"
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def convert_html_to_text(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    for tag in soup(['script', 'style', 'sup']):
        tag.decompose()
    return soup.get_text(separator=' ', strip=True)

def gemini_summarize(plain_text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"Summarize this:\n\n{plain_text}")
    try:
        return response.text
    except AttributeError:
        return "Failed to generate summary."


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <Wikipedia_Title>")
        sys.exit(1)

    title = sys.argv[1]
    print(f"Fetching Wikipedia page for: {title}")

    try:
        html = fetch_wikipedia(title)
        text = convert_html_to_text(html)
        summary = gemini_summarize(text)
        print(json.dumps({"summary": summary}, indent=2))

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
