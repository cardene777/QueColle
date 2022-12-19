# QueColle

```sh
question collection
```

## Command

```sh
python manage.py makemigrations && python manage.py migrate && python manage.py createsuperuser
```

```sh
python manage.py loaddata question/fixture/question_collection.json && python manage.py loaddata question/fixture/question.json && python manage.py loaddata question/fixture/data.json
```
```sh
python manage.py runserver
```

## 参考サイト
[docker-composeでDjango開発環境を構築する
](https://zenn.dev/dsonoda/articles/dbe14ca8af617ed85b1f#docker-compose%E3%82%92%E5%AE%9F%E8%A1%8C%E3%81%97%E3%81%A6%E3%82%B7%E3%82%B9%E3%83%86%E3%83%A0%E3%82%92%E8%B5%B7%E5%8B%95%E3%80%81%E3%82%A2%E3%83%83%E3%83%97%E3%83%AD%E3%83%BC%E3%83%89%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%81%AE%E6%B0%B8%E7%B6%9A%E5%8C%96%E3%82%92%E7%A2%BA%E8%AA%8D)
