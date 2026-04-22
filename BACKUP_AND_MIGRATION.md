# 📦 Backup & Migration Guide

## 📌 Project Overview

This project is built with Django and deployed on Render.

- ⚙️ Backend: Django
- 🗄️ Database: PostgreSQL (Neon)
- ☁️ Media Storage: Cloudinary
- 🚀 Hosting: Render

---

## 1️⃣ 🗄️ Database Information

Production database is hosted on PostgreSQL (Neon).

🔗 Connection string format:

```bash
postgresql://<user>:<password>@<host>/<dbname>?sslmode=require
2️⃣ 💾 Database Backup
✅ Using pg_dump (Recommended)

Run:

pg_dump "postgresql://neondb_owner:<PASSWORD>@ep-xxx.ap-southeast-1.aws.neon.tech/neondb?sslmode=require" > backup.sql

📌 Notes:

Replace <PASSWORD> with the actual database password
This will generate a full backup file: backup.sql
3️⃣ ♻️ Database Restore

Run:

psql "postgresql://neondb_owner:<PASSWORD>@ep-xxx.ap-southeast-1.aws.neon.tech/neondb?sslmode=require" < backup.sql
4️⃣ 💻 Local Development Setup
📥 Setup Steps
Clone the repository
Create .env from .env.example
▶️ Run commands:
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

5️⃣ 🚀 Deployment (Render)

Platform: Render

🛠️ Build Command
pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput && python manage.py setup_admin
▶️ Start Command
gunicorn toparch_site.wsgi:application

📌 Environment variables must be configured in the Render dashboard.

6️⃣ 🔐 Environment Variables

Required variables (see .env.example):

SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=
DATABASE_URL=
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

7️⃣ 📂 Static & Media Files
📦 Static files → served using WhiteNoise
🖼️ Media files → stored on Cloudinary
8️⃣ ⚠️ Notes
🧪 Local uses SQLite if DATABASE_URL is not set
🌐 Production uses PostgreSQL (Neon)
💾 Always backup database before major updates
🔒 Never commit real secrets to GitHub
