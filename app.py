from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    notes = db.relationship('Note', backref='user', lazy=True)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/ml-learn')
def ml_learn():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/web-dev')
def web_dev():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('web_dev.html')

@app.route('/ai')
def ai():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('ai.html')

@app.route('/app-dev')
def app_dev():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('app_dev.html')

@app.route('/cyber-sec')
def cyber_sec():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('cyber_sec.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('home'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            return 'Username already exists'
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/notes', methods=['GET', 'POST'])
def notes():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        content = request.form['content']
        new_note = Note(content=content, user_id=user.id)
        db.session.add(new_note)
        db.session.commit()
    notes = Note.query.filter_by(user_id=user.id).all()
    return render_template('notes.html', notes=notes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
