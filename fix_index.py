html_content = """{% extends "base.html" %}

{% block content %}

<!-- Блок Цитата дня -->
{% if quote %}
<div class="quote-of-day">
    <p>«{{ quote.text }}»</p>
    <span class="author">— {{ quote.writer.name }}</span>
</div>
{% endif %}

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

with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Файл index.html успешно перезаписан! Теперь там нет дублей.")