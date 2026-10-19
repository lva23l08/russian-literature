from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from models import db, Writer, Book, Quote, User
import random

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def index():
    writers = Writer.query.all()
    quotes = Quote.query.all()
    quote_of_day = random.choice(quotes) if quotes else None
    return render_template('index.html', writers=writers, quote=quote_of_day)

@app.route('/writer/<int:writer_id>')
def writer_page(writer_id):
    writer = Writer.query.get_or_404(writer_id)
    books = Book.query.filter_by(writer_id=writer.id).all()
    return render_template('writer.html', writer=writer, books=books)

# --- АВТОРИЗАЦИЯ ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Проверка, есть ли уже такой пользователь
        user_exists = User.query.filter((User.username == username) | (User.email == email)).first()
        if user_exists:
            flash('Пользователь с таким именем или email уже существует', 'error')
            return redirect(url_for('register'))
            
        new_user = User(username=username, email=email)
        new_user.set_password(password) # Хешируем пароль!
        db.session.add(new_user)
        db.session.commit()
        
        flash('Регистрация успешна! Теперь войдите.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Добро пожаловать, {user.username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверный email или пароль', 'error')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из системы', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)