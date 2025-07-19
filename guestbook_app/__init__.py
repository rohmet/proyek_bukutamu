# guestbook_app/__init__.py

from flask import Flask, session
from .models import db, User

def create_app():
    app = Flask(__name__)
    
    # Konfigurasi aplikasi
    app.config['SECRET_KEY'] = 'ini-adalah-kunci-rahasia-yang-sulit-ditebak'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///buku_tamu.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inisialisasi database
    db.init_app(app)

    # Mengimpor dan mendaftarkan Blueprints
    from .auth.routes import auth_bp
    from .guestbook.routes import guestbook_bp
    from .profile.routes import profile_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(guestbook_bp)
    app.register_blueprint(profile_bp)

    # Context processor untuk inject current_user ke semua template
    @app.context_processor
    def inject_user():
        user_id = session.get('user_id')
        if user_id:
            return dict(current_user=User.query.get(user_id))
        return dict(current_user=None)
        
    with app.app_context():
        # Membuat semua tabel database jika belum ada
        db.create_all()

    return app