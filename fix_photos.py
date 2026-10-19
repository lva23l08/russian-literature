from app import app
from models import db, Writer

with app.app_context():
    # Берем всех писателей из базы по порядку
    writers = Writer.query.order_by(Writer.id).all()
    
    # Присваиваем им картинки 1.jpg, 2.jpg и т.д.
    for i, writer in enumerate(writers, start=1):
        writer.photo = f"{i}.jpg"
        
    db.session.commit()
    print(f"Успешно! Картинки привязаны к {len(writers)} писателям.")