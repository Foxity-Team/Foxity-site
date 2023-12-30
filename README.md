## Генерация сайта

1. Создайте venv через команду:

```bash
python -m venv env
source env/bin/activate
```

2. Установите зависимости

```bash
pip install -r requirements.txt
```

3. Собберите сайт

```bash
python generate-news.py
```

Выходной сайт будет сгенерирован в папке `public/` вместе с папкой `static` скопированной в `public/static`
