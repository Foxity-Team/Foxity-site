from markdown import markdown
from os import listdir

def render_news():
    news = []
    files = listdir("news/")

    for file in files:
        index = int(file.split("#")[0])
        post = open("news/"+file, "r", encoding='utf-8').read()

        news.append((
            index,
            markdown(post)
        ))
    return sorted(news, key=lambda x: x[0], reverse=True)