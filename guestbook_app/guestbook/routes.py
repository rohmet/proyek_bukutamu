# guestbook_app/guestbook/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from guestbook_app.models import db, Pesan
from guestbook_app.auth.routes import login_required

# Membuat Blueprint 'guestbook'
guestbook_bp = Blueprint('guestbook', __name__, template_folder='templates')

@guestbook_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():    
  if request.method == 'POST':
    pesan_text = request.form['pesan']
    user_id = session['user_id']
    pesan_baru = Pesan(pesan=pesan_text, user_id=user_id)
    try:
      db.session.add(pesan_baru)
      db.session.commit()
      flash('Pesan berhasil disimpan!', 'success')
    except:
      db.session.rollback()
      flash("Terjadi kesalahan saat menyimpan pesan.", 'danger')
    return redirect(url_for('guestbook.index'))
  else:
    semua_pesan = Pesan.query.order_by(Pesan.id.desc()).all()
    return render_template('index.html', semua_pesan=semua_pesan)

@guestbook_bp.route('/hapus/<int:id>', methods=['POST'])
@login_required
def hapus(id):
  pesan = Pesan.query.get_or_404(id)
  # Pastikan hanya user yang membuat pesan yang bisa menghapus
  if pesan.user_id != session['user_id']:
      flash('Anda tidak memiliki izin untuk menghapus pesan ini!', 'danger')
      return redirect(url_for('guestbook.index'))
  try:
    db.session.delete(pesan)
    db.session.commit()
    flash('Pesan berhasil dihapus!', 'success')
  except:
    db.session.rollback()
    flash("Terjadi kesalahan saat menghapus pesan.", 'danger')
  return redirect(url_for('guestbook.index'))

@guestbook_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
  pesan = Pesan.query.get_or_404(id)
  # Pastikan hanya user yang membuat pesan yang bisa mengedit
  if pesan.user_id != session['user_id']:
      flash('Anda tidak memiliki izin untuk mengedit pesan ini!', 'danger')
      return redirect(url_for('guestbook.index'))

  if request.method == 'POST':
    pesan.pesan = request.form['pesan']
    try:
      db.session.commit()
      flash('Pesan berhasil diedit!', 'success')
      return redirect(url_for('guestbook.index'))
    except:
      db.session.rollback()
      flash("Terjadi kesalahan saat mengedit pesan.", 'danger')
  return render_template('edit.html', pesan=pesan)