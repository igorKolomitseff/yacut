# Проект YaCut - сервис укорачивания ссылок

## Функции проекта

* ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает 
сам пользователь или предоставляет сервис. 

## Стек технологий
* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/3.0.x/)

## Как развернуть проект
1. Клонируйте репозиторий и перейдите в директорию yacut
```bash
git git@github.com:igorKolomitseff/yacut.git
cd yacut
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python3 -m venv venv
source venv/bin/activate  # Для Linux и macOS
source venv/Scripts/activate  # Для Windows
```

3. Обновите pip и установите зависимости проекта:
```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
4. Создайте .env файл в корневой директории и заполните его данными в соответствии с файлом .env.example

5. Создайте файл базы данных командой:
```bash
flask db upgrade
```
Файл будет создан в директории instance/

6. Запустите проект:
```bash
flask run
```
Откройте браузер и перейдите по адресу http://127.0.0.1:5000 для доступа главной странице проекта

### Автор

[Игорь Коломыцев](https://github.com/igorKolomitseff)