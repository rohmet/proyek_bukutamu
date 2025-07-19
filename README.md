Tentu, saya akan perbaiki penulisannya ke dalam format Markdown yang rapi dan terstruktur.

-----

# Aplikasi Buku Tamu (Guestbook) dengan Flask

Ini adalah aplikasi web sederhana "Buku Tamu" yang dibangun menggunakan *framework* Flask di Python. Proyek ini didesain dengan struktur yang modular dan terorganisir menggunakan **Flask Blueprints** untuk memisahkan logika aplikasi ke dalam komponen-komponen yang dapat dikelola dengan mudah.

Pengguna dapat mendaftar, login, dan meninggalkan pesan. Pengguna yang terautentikasi juga dapat mengedit atau menghapus pesan yang mereka buat sendiri.

## Fitur Utama

  - **Autentikasi Pengguna**:
      - Registrasi pengguna baru.
      - Login dan Logout.
      - Sesi pengguna yang aman.
      - *Password* disimpan menggunakan *hashing* yang aman (PBKDF2).
  - **Manajemen Pesan (CRUD)**:
      - **Create**: Pengguna yang sudah login dapat memposting pesan baru.
      - **Read**: Semua pesan ditampilkan di halaman utama, diurutkan dari yang terbaru.
      - **Update**: Pengguna dapat mengedit pesan mereka sendiri.
      - **Delete**: Pengguna dapat menghapus pesan mereka sendiri.
  - **Profil Pengguna**: Halaman profil sederhana yang menampilkan semua pesan dari seorang pengguna.
  - **Rute Terproteksi**: Halaman dan aksi tertentu (seperti memposting pesan) hanya dapat diakses setelah login.
  - **Notifikasi Flash**: Memberikan umpan balik kepada pengguna setelah melakukan aksi (misalnya, "Login berhasil\!", "Pesan berhasil dihapus\!").

## Teknologi yang Digunakan

  - **Backend**: [Flask](https://flask.palletsprojects.com/)
  - **Database ORM**: [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
  - **Database Engine**: [SQLite](https://www.sqlite.org/index.html)
  - **Templating**: [Jinja2](https://jinja.palletsprojects.com/)
  - **Password Hashing**: [Werkzeug](https://werkzeug.palletsprojects.com/)

## Struktur Proyek

Proyek ini menggunakan pola *Application Factory* dan *Blueprints* untuk skalabilitas dan keteraturan kode.

```
/project_folder
|-- /guestbook_app
|   |-- __init__.py         # Application Factory (create_app)
|   |-- models.py           # Model database (User, Pesan)
|   |-- /auth
|   |   |-- __init__.py
|   |   `-- routes.py       # Rute untuk autentikasi
|   |-- /guestbook
|   |   |-- __init__.py
|   |   `-- routes.py       # Rute untuk fungsionalitas buku tamu
|   |-- /profile
|   |   |-- __init__.py
|   |   `-- routes.py       # Rute untuk profil pengguna
|   |-- /static/            # File statis (CSS, JS, gambar)
|   `-- /templates/         # Template HTML
|       |-- index.html
|       |-- edit.html
|       |-- login.html
|       |-- register.html
|       `-- profil.html
|
|-- requirements.txt        # Daftar dependensi Python
`-- run.py                  # Titik masuk untuk menjalankan aplikasi
```

## Instalasi dan Konfigurasi

Untuk menjalankan proyek ini di lingkungan lokal Anda, ikuti langkah-langkah berikut:

1.  **Clone Repositori**

    ```bash
    git clone [URL-repositori-anda]
    cd [nama-folder-proyek]
    ```

2.  **Buat dan Aktifkan Virtual Environment**
    Ini adalah praktik terbaik untuk mengisolasi dependensi proyek.

      - **Windows**:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
      - **macOS / Linux**:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install Dependensi**
    Buat file `requirements.txt` dengan konten berikut:

    ```txt
    Flask
    Flask-SQLAlchemy
    ```

    Kemudian, instal dependensi menggunakan `pip`:

    ```bash
    pip install -r requirements.txt
    ```

## Menjalankan Aplikasi

Setelah semua dependensi terinstal, jalankan aplikasi dengan perintah berikut dari direktori utama proyek:

```bash
python run.py
```

Aplikasi akan berjalan dalam mode *debug* dan dapat diakses di **[http://127.0.0.1:5000](https://www.google.com/search?q=http://127.0.0.1:5000)** pada peramban Anda.

Database SQLite (`buku_tamu.db`) akan secara otomatis dibuat di direktori utama saat aplikasi pertama kali dijalankan.
