from app import app, db

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Создаем таблицу пользователей в базе данных
    app.run(debug=True)
