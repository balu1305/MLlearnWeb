from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

def get_user_db_path(user_id):
    return os.path.join('user_dbs', f'user_{user_id}.db')

def get_user_db_session(user_id):
    user_db_path = get_user_db_path(user_id)
    engine = db.create_engine(f'sqlite:///{user_db_path}')
    session_factory = sessionmaker(bind=engine)
    return scoped_session(session_factory)

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
        user_db_path = get_user_db_path(new_user.id)
        if not os.path.exists(user_db_path):
            engine = db.create_engine(f'sqlite:///{user_db_path}')
            db.metadata.create_all(engine)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/notes', methods=['GET', 'POST'])
def notes():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    user_db_session = get_user_db_session(user_id)
    Note = db.Table('note', db.metadata, autoload_with=user_db_session.bind)
    if request.method == 'POST':
        content = request.form['content']
        new_note = Note.insert().values(content=content, user_id=user_id)
        user_db_session.execute(new_note)
        user_db_session.commit()
    notes = user_db_session.query(Note).filter_by(user_id=user_id).all()
    return render_template('notes.html', notes=notes)

if __name__ == '__main__':
    if not os.path.exists('user_dbs'):
        os.makedirs('user_dbs')
    with app.app_context():
        db.create_all()
    app.run(debug=True)