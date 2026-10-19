import os

# Создаем нужные папки, если их нет
os.makedirs("templates", exist_ok=True)
os.makedirs("static/css", exist_ok=True)

files = {}

# 1. Файл app.py
files["app.py"] = """from flask import Flask, render_template
from config import Config
from models import db, Writer, Book

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def index():
    writers = Writer.query.all()
    return render_template('index.html', writers=writers)

@app.route('/writer/<int:writer_id>')
def writer_page(writer_id):
    writer = Writer.query.get_or_404(writer_id)
    books = Book.query.filter_by(writer_id=writer.id).all()
    return render_template('writer.html', writer=writer, books=books)

if __name__ == '__main__':
    app.run(debug=True)
"""

# 2. Файл base.html
files["templates/base.html"] = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Русская литература</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <header>
        <h1><a href="/">Русская литература</a></h1>
        <nav>
            <a href="/">Главная</a>
            <a href="#">Цитатник</a>
            <a href="#">Вход</a>
        </nav>
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        <p>© 2026 Сайт «Русская литература»</p>
    </footer>
</body>
</html>
"""

# 3. Файл index.html
files["templates/index.html"] = """{% extends "base.html" %}

{% block content %}
<h2 style="text-align: center; margin-bottom: 20px;">Галерея писателей</h2>

<div class="gallery">
    {% for writer in writers %}
    <a href="/writer/{{ writer.id }}" class="card">
        {% if writer.photo %}
            <img src="{{ url_for('static', filename='images/' + writer.photo) }}" alt="{{ writer.name }}" class="writer-photo">
        {% else %}
            <div class="photo-placeholder"></div>
        {% endif %}
        
        <h3>{{ writer.name }}</h3>
        <p class="years">{{ writer.years }}</p>
        <p class="era">{{ writer.era }}</p>
    </a>
    {% endfor %}
</div>
{% endblock %}
"""

# 4. Файл writer.html
files["templates/writer.html"] = """{% extends "base.html" %}

{% block content %}
<div class="writer-page">
    <div class="writer-header">
        {% if writer.photo %}
            <img src="{{ url_for('static', filename='images/' + writer.photo) }}" alt="{{ writer.name }}" class="writer-portrait">
        {% endif %}
        <div class="writer-info">
            <h1>{{ writer.name }}</h1>
            <p class="years">{{ writer.years }}</p>
            <p class="bio">{{ writer.bio }}</p>
            <a href="/" class="btn-back">← Назад к галерее</a>
        </div>
    </div>

    <h2>Произведения</h2>
    <div class="books-grid">
        {% for book in books %}
        <div class="book-card">
            <div class="book-cover">
                <h3>{{ book.title }}</h3>
            </div>
            <p class="book-year">{{ book.year }} г.</p>
            <p class="book-plot">{{ book.plot }}</p>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
"""

# 5. Файл style.css
files["static/css/style.css"] = """* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: 'Georgia', serif;
    background-color: #f4f4f4;
    color: #222;
}

header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 40px;
    border-bottom: 2px solid #222;
    background: #fff;
}

header h1 a {
    text-decoration: none;
    color: #000;
    font-size: 28px;
    letter-spacing: 2px;
}

nav a {
    margin-left: 20px;
    text-decoration: none;
    color: #333;
    font-weight: bold;
    transition: color 0.3s;
}

nav a:hover {
    color: #888;
}

main {
    padding: 40px;
}

/* Горизонтальная галерея */
.gallery {
    display: flex;
    overflow-x: auto;
    gap: 30px;
    padding-bottom: 20px;
}

.card {
    min-width: 220px;
    text-align: center;
    background: #fff;
    padding: 20px;
    border: 1px solid #ccc;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    transition: transform 0.4s ease, box-shadow 0.4s ease;
    cursor: pointer;
    text-decoration: none;
    color: inherit;
    display: block;
}

.card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 15px 30px rgba(0,0,0,0.2);
    border-color: #000;
}

.writer-photo {
    width: 160px;
    height: 200px;
    object-fit: cover;
    margin: 0 auto 15px auto;
    border: 1px solid #999;
    filter: grayscale(100%);
    transition: filter 0.3s;
}

.card:hover .writer-photo {
    filter: grayscale(0%);
}

.photo-placeholder {
    width: 160px;
    height: 200px;
    background-color: #ddd;
    margin: 0 auto 15px auto;
    border: 1px solid #999;
}

.card h3 {
    font-size: 18px;
    margin-bottom: 5px;
}

.years {
    color: #555;
    font-size: 14px;
    font-style: italic;
}

.era {
    font-size: 12px;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 5px;
}

footer {
    text-align: center;
    padding: 20px;
    border-top: 1px solid #ccc;
    margin-top: 40px;
    color: #666;
    font-size: 14px;
}

/* Стили для страницы писателя */
.writer-header {
    display: flex;
    gap: 40px;
    align-items: flex-start;
    margin-bottom: 40px;
    background: #fff;
    padding: 30px;
    border: 1px solid #ddd;
}

.writer-portrait {
    width: 250px;
    filter: grayscale(100%);
    border: 1px solid #999;
}

.writer-info h1 {
    margin-bottom: 10px;
}

.bio {
    margin: 20px 0;
    font-size: 16px;
    line-height: 1.6;
}

.btn-back {
    color: #333;
    text-decoration: none;
    border-bottom: 1px solid #333;
    padding-bottom: 2px;
}

.books-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    margin-top: 20px;
}

.book-card {
    background: #fff;
    border: 1px solid #ccc;
    padding: 20px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    transition: transform 0.3s;
}

.book-card:hover {
    transform: scale(1.03);
}

.book-cover {
    background: #222;
    color: #fff;
    height: 150px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    margin-bottom: 15px;
    padding: 10px;
    box-shadow: inset -5px 0 10px rgba(0,0,0,0.5);
}

.book-year {
    color: #888;
    font-size: 14px;
    margin-bottom: 10px;
}

.book-plot {
    font-size: 14px;
    color: #444;
}
"""

# Записываем все файлы на диск
for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Обновлен файл: {path}")

print("\\nВсе файлы успешно обновлены и сохранены!")