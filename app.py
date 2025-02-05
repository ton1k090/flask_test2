from datetime import datetime

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db' # Cоздать бд
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):

    '''Класс записей создание табличек в БД'''
    id = db.Column(db.Integer, primary_key=True) # primary key - уникальность поля
    title = db.Column(db.String(80), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow) # Со значением по умолчанию

    def __repr__(self):
        '''Будет выдаваться сам объект и его айди'''
        return '<Article %r>' % self.id



@app.route('/home')
@app.route('/')
def index():
    '''Хендлер домашней страницы'''
    return render_template('index.html')


@app.route('/about')
def about():
    '''Хендлер страницы о нас'''
    return render_template('about.html')


@app.route('/create-article', methods=['GET', 'POST']) # Методы гет и пост
def create_article():
    '''Записывает данные в БД'''
    if request.method == 'POST':
        title = request.form['title'] # получение из формы
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)  # Сама запись данных
        try:
            db.session.add(article) # Добавляем в сессию
            db.session.commit() # Коммитим изменения
            return redirect('/') # Если ок переадресуем на глав страницу
        except:
            return 'Errors'
    else:

        '''Хендлер страницы о нас'''
        return render_template('create_article.html')









with app.app_context():
    db.create_all()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)