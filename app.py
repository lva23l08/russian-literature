from flask import Flask, render_template
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
