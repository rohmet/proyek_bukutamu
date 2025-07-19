from flask import Flask, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ini-adalah-kunci-rahasia-yang-sulit-ditebak'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///buku_tamu.db'
db = SQLAlchemy(app)

# Model untuk Buku Tamu
class Pesan(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nama = db.Column(db.String(100), nullable=False)
  pesan = db.Column(db.Text, nullable=False)

  # fungsi untuk merepresentasikan objek Pesan
  def __repr__(self):
      return f'<Pesan {self.id}>'

# Model untuk User
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)

  def __repr__(self):
    return f'<User {self.username}>'

# proteksi route dengan login
def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if 'user_id' not in session:
      flash('Anda harus login terlebih dahulu!', 'danger')
      return redirect(url_for('login'))
    return f(*args, **kwargs)
  return decorated_function

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():    
  if request.method == 'POST':
    name = request.form['nama']
    pesan = request.form['pesan']

    pesan_baru = Pesan(nama=name, pesan=pesan)
    
    try:
      db.session.add(pesan_baru)
      db.session.commit()
      flash('Pesan berhasil disimpan!', 'success')
      return redirect(url_for('index'))
    except:
      db.session.rollback()
      return "Terjadi kesalahan saat menyimpan pesan."
  else:
    semua_pesan = Pesan.query.order_by(Pesan.id.desc()).all()
    return render_template('index.html', semua_pesan=semua_pesan)

# Route untuk menghapus pesan
@app.route('/hapus/<int:id>', methods=['POST'])
@login_required
def hapus(id):
  pesan = Pesan.query.get_or_404(id)
  try:
    db.session.delete(pesan)
    db.session.commit()
    flash('Pesan berhasil dihapus!', 'success')
    return redirect(url_for('index'))
  except:
    db.session.rollback()
    return "Terjadi kesalahan saat menghapus pesan."

# Route untuk mengedit pesan
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
  pesan = Pesan.query.get_or_404(id)
  if request.method == 'POST':
    pesan.nama = request.form['nama']
    pesan.pesan = request.form['pesan']
    
    try:
      db.session.commit()
      flash('Pesan berhasil diedit!', 'success')
      return redirect(url_for('index'))
    except:
      db.session.rollback()
      return "Terjadi kesalahan saat mengedit pesan."
  else:
    return render_template('edit.html', pesan=pesan)

# Route untuk halaman registrasi
@app.route('/register', methods=['GET', 'POST'])
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
      return redirect(url_for('login'))
    except:
      db.session.rollback()
      return "Terjadi kesalahan saat mendaftarkan user."
  return render_template('register.html')
    
# Route untuk halaman login
@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
      session['user_id'] = user.id
      flash('Login berhasil!', 'success')
      return redirect(url_for('index'))
    else:
      flash('Username atau password salah.', 'danger')
  return render_template('login.html')

# Route untuk logout
@app.route('/logout')
@login_required
def logout():
  session.pop('user_id', None)
  flash('Anda telah logout.', 'success')
  return redirect(url_for('login'))

@app.context_processor
def inject_user():
  user_id = session.get('user_id')
  if user_id:
    user = User.query.get(user_id)
    return dict(current_user=user)
  return dict(current_user=None)

if __name__ == '__main__':
  app.run(debug=True)