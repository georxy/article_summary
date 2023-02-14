import openai
import re
import requests
from bs4 import BeautifulSoup

max_tokes = 4097
char_per_token = 4


def article_summ(article_request):

    if article_request == "Article not found.":
        return "Article not found."
    else:
        email_pitch_request = f'write down a quick summary of main points (make sure to include data ' \
                              f'from the article) of this article: \n{article_request}'

        openai.api_key = "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"
        request = openai.Completion.create(
            engine="text-davinci-003",
            prompt=email_pitch_request,
            temperature=0.7,
            max_tokens=200,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0)
        response = str(request)
        text_start_pos_search = re.search('"text": "', response)
        text_start_pos = int(text_start_pos_search.end())
        text_string_0 = response[text_start_pos:]
        text_end_pos_search = re.search('}', text_string_0)
        text_end_pos = int(text_end_pos_search.start()) - 6
        text_string = str(text_string_0[:text_end_pos])
        text0 = text_string.replace('\\n', '\n')
        text = text0.replace('\\', '')
        return text


def request_article(url):
    try:
        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the main content of the article by searching for common HTML elements
        article = soup.find('div', {'class': 'article-body'})
        if not article:
            article = soup.find('div', {'id': 'main-content'})
        if not article:
            article = soup.find('div', {'class': 'entry-content'})
        if not article:
            article = soup.find('article')
        if not article:
            article = soup.find('section', {'class': 'main-section'})
        if not article:
            article = soup.find('div', {'class': 'post-content'})
        if not article:
            article = soup.find('div', {'class': 'content'})
        if not article:
            article = soup.find('div', {'id': 'content'})

        if article:
            return article.text[:max_tokes*char_per_token - 10]
        else:
            return "Article not found."
    except Exception as e:
        return e


def return_summary(website_url):
    return article_summ(request_article(website_url))
