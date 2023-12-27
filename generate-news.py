import os
import marko

generated_news_dir = 'public/news/'
news_dir = 'news/'

mds = []
files = []

with open(news_dir + 'news-template.html') as f:
    news_template = f.read()

with open(news_dir + 'index-template.html') as f:
    index_template = f.read()

index_contents = '<ul>'

if not os.path.exists(generated_news_dir):
    os.mkdir(generated_news_dir)

for filename in os.listdir(generated_news_dir):
    os.remove(generated_news_dir + filename)

for filename in os.listdir(news_dir):
    base, ext = os.path.splitext(filename)
    if ext != '.md': continue

    files.append(base)
    with open(news_dir + filename) as f:
        mds.append(f.read())

for (filename, txt) in zip(files, [marko.convert(txt) for txt in mds]):
    template = news_template.replace('{{ body }}', txt)
    index_contents += f'<li><a href="/{news_dir}{filename}.html">{filename}</a></li>'
    print(f'File: {filename}')
    print(template)
    with open(generated_news_dir + filename + '.html', 'w') as f:
        f.write(template)

index_contents += '</ul>'

with open(generated_news_dir + 'index.html', 'w') as f:
    f.write(index_template.replace('{{ body }}', index_contents))

print(f'Сгенерировано {len(files) + 1} файлов')
