from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

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


@app.route('/', methods=['GET', 'POST'])
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

if __name__ == '__main__':
  app.run(debug=True)