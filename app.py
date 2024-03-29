from flask import Flask
from routes import register_routes

app = Flask(__name__)
# Защита от атаки подделки межсайтовых запросов
app.config.from_object("defender")

register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
