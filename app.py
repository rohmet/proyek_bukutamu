from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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
      return redirect(url_for('index'))
    except:
      db.session.rollback()
      return "Terjadi kesalahan saat menyimpan pesan.", 500
  else:
    semua_pesan = Pesan.query.order_by(Pesan.id.desc()).all()
    return render_template('index.html', semua_pesan=semua_pesan)

if __name__ == '__main__':
  app.run(debug=True)