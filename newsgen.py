from markdown import markdown
from os import listdir

def renderNews():
    news = []
    files = listdir("news/")
    files.sort(key=max)

    for file in files:
        index = int(file.split("#")[0])
        post = open("news/"+file, "r").read()

        news.append((
            index,
            markdown(post)
        ))
    
    return sorted(news, key=lambda x: x[0], reverse=True)