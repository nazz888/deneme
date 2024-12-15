from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite kullanımı
app.config['SECRET_KEY'] = 'your_secret_key'  # Uygulama için gizli anahtar

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Kullanıcı modelini oluşturmak için models.py'yi kontrol edin.
from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Ana sayfa rotası
@app.route('/')
def home():
    return render_template('base.html')

# Kayıt olma rotası
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Kullanıcı adı daha önce alınmış mı kontrol et
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Bu kullanıcı adı zaten alınmış. Lütfen başka bir kullanıcı adı deneyin.', 'danger')
            return redirect(url_for('register'))

        # Şifreyi hashleyip kullanıcıyı veritabanına ekle
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Kayıt başarılı! Şimdi giriş yapabilirsiniz.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Giriş rotası
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Başarıyla giriş yaptınız!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Kullanıcı adı veya şifre yanlış.', 'danger')
    return render_template('login.html')

# Dashboard rotası (korumalı rota)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

# Çıkış rotası
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Çıkış yaptınız.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
