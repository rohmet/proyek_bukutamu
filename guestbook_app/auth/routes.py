# guestbook_app/auth/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from guestbook_app.models import db, User
from functools import wraps

# Membuat Blueprint 'auth'
auth_bp = Blueprint('auth', __name__, template_folder='templates')

# Dekorator untuk proteksi route
def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if 'user_id' not in session:
      flash('Anda harus login terlebih dahulu!', 'danger')
      return redirect(url_for('auth.login'))
    return f(*args, **kwargs)
  return decorated_function

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    user_baru = User(username=username, password=hashed_password)
    try:
      db.session.add(user_baru)
      db.session.commit()
      flash('User berhasil didaftarkan!', 'success')
      return redirect(url_for('auth.login'))
    except:
      db.session.rollback()
      flash("Username sudah digunakan atau terjadi kesalahan.", 'danger')
      return redirect(url_for('auth.register'))
  return render_template('register.html')
    
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
      session['user_id'] = user.id
      flash('Login berhasil!', 'success')
      return redirect(url_for('guestbook.index'))
    else:
      flash('Username atau password salah.', 'danger')
  return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
  session.pop('user_id', None)
  flash('Anda telah logout.', 'success')
  return redirect(url_for('auth.login'))