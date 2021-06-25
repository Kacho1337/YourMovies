from flask import Flask, redirect,url_for, render_template, request, session,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = "python"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.sqlite3'
db = SQLAlchemy(app)

class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Movie = db.Column(db.String(50), nullable=False)
    Year = db.Column(db.Integer, nullable=False)
    Rating = db.Column(db.Float, nullable=False)

    def __str__(self):
        return f'{self.Movie} {self.Year}  {self.Rating}'




@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('user'))

    return render_template('login.html')


@app.route('/user')
def user():
    all_movies=Movies.query.all()
    return render_template('user.html',all_movies=all_movies)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('index.html')

@app.route('/movies', methods=['GET', 'POST'])
def movies():
    if request.method == 'POST':
        m = request.form['Movie']
        y = request.form['Year']
        r = request.form['Rating']
        f1 = Movies(Movie=m, Year=int(y), Rating=float(r))
        db.session.add(f1)
        db.session.commit()
        flash('ფილმი / სერიალი დამატებულია')

    return render_template('movies.html')


if __name__ == "__main__":
    app.run()