from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@app.route('/')
def home():
    if 'user_id' in session:
        return render_template('home.html', user=session.get('username'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('User already exists! Try another username.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))

        flash('Invalid credentials! Try again.', 'danger')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('home.html', user=session.get('username'))
    flash('Please log in first!', 'warning')
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route("/home.html")
def homemain():
    return render_template('home.html')

@app.route("/BrowseBooks1.html")
def browsebooks():
    return render_template('BrowseBooks1.html')

@app.route("/SellBooks.html")
def sellbooks():
    return render_template('SellBooks.html')

@app.route("/Contact.html")
def contact():
    return render_template('Contact.html')

@app.route("/community.html")
def community_redirect():
    return redirect("/Contact.html")

@app.route("/About.html")
def About():
    return render_template('About.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
