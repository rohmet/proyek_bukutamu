# guestbook_app/profile/routes.py

from flask import Blueprint, render_template
from guestbook_app.models import User
from guestbook_app.auth.routes import login_required

profile_bp = Blueprint('profile', __name__, template_folder='templates')

@profile_bp.route('/profile/<string:username>')
@login_required
def user_profile(username):
  user = User.query.filter_by(username=username).first_or_404()
  return render_template('profil.html', user=user)