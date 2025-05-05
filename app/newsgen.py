from markdown import markdown
from os import listdir
import os.path

news_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "news")

def render_news():
    news = []
    files = listdir(news_dir)

    for file in files:
        index = int(file.split("#")[0])
        post = open(os.path.join(news_dir, file), "r", encoding='utf-8').read()

        news.append((
            index,
            markdown(post)
        ))
    return sorted(news, key=lambda x: x[0], reverse=True)