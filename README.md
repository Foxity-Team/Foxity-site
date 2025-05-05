## Развёртка сайта

### Подготовка
1. Склонируйте репо: `git clone http://foxityteam-repo.i2p/Foxity/Foxity-site.git`
2. Скопируйте .env.template в .env и подставьте свои значения
### Через Docker
`docker compose up` Для разработки и тестов, НЕ ИСПОЛЬЗОВАТЬ НА ПРОДЕ!

`docker compose -f docker-compose.prod.yml up` Для прода: имеется health check, приложение запускается через gunicorn. Можно изменять темплейты и новости (проброшены волюмы).
### Вручную
1. Создайте venv через команду:

```bash
python -m venv env
source env/bin/activate
```

2. Установите зависимости

```bash
pip install -r requirements.txt
```

3. Запустите сайт

```bash
python flask-server.py # (для тестов и дева)
gunicorn --config gunicorn.conf.py -w 4 -b хост:порт flask-server:app # для прода
```

## Публикация новостей
Для публикации новостей нужно создать новый markdown файл в папке news: `<индекс># <название>.md`  
Затем можно приступить к редактированию, используя стандартный синтаксис markdown.