# ⚡ Productivity Hub

A full-featured, mobile-responsive Django productivity application with:

- ✅ **Tasks** – create, prioritize, track status, attachments
- 🎯 **Goals** – set targets, track progress with images
- 🔥 **Habits** – daily/weekly tracking with one-tap check-in
- 📝 **Notes** – colorful pinned notes with attachments
- 📅 **Calendar** – events with time, location, colors
- 💰 **Expense Tracker** – income/expense with categories & receipts
- 👤 **User accounts** – register, login, profile with avatar

Fully prepared for **Render.com** production deployment (PostgreSQL + Gunicorn + WhiteNoise).

---

## Quick Start (Local)

```bash
# 1. Clone / unzip and enter folder
cd productivity_app   # or the extracted folder

# 2. Create virtualenv (recommended)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Environment
cp .env.example .env
# Edit .env if needed (SECRET_KEY, etc.)

# 5. Migrate & run
python manage.py migrate
python manage.py createsuperuser   # optional
python manage.py runserver
```

Open http://127.0.0.1:8000

---

## Deploy to Render.com (Step-by-step)

### Option A – Blueprint (recommended)

1. Push this project to a **GitHub** repository.
2. Go to [Render Dashboard](https://dashboard.render.com) → **New** → **Blueprint**.
3. Connect your GitHub repo. Render will read `render.yaml`.
4. It will create:
   - A **Web Service** (`productivity-app`)
   - A **PostgreSQL** database (`productivity-db`)
5. Click **Apply**. Wait for the first deploy to finish.

### Option B – Manual setup

1. **Create PostgreSQL database**
   - Dashboard → **New** → **PostgreSQL**
   - Name: `productivity-db`
   - Plan: Free
   - Note the **Internal Database URL**.

2. **Create Web Service**
   - Dashboard → **New** → **Web Service**
   - Connect the GitHub repo
   - Settings:
     | Field | Value |
     |-------|-------|
     | Name | productivity-app |
     | Runtime | Python 3 |
     | Build Command | `./build.sh` |
     | Start Command | `gunicorn productivity_app.wsgi:application --bind 0.0.0.0:$PORT` |
     | Plan | Free |

3. **Environment Variables** (Dashboard → Environment)

   | Key | Value |
   |-----|-------|
   | `SECRET_KEY` | Click **Generate** or paste a long random string |
   | `DEBUG` | `False` |
   | `ALLOWED_HOSTS` | `.onrender.com` (or your custom domain) |
   | `CSRF_TRUSTED_ORIGINS` | `https://your-app-name.onrender.com` |
   | `DATABASE_URL` | Copy from the PostgreSQL service (Internal Database URL) |
   | `PYTHON_VERSION` | `3.12.3` |
   | `WEB_CONCURRENCY` | `2` |

4. Click **Create Web Service**. Render runs `build.sh` (install → collectstatic → migrate) then starts Gunicorn.

### After first deploy

- Visit `https://your-app-name.onrender.com`
- Register a new user or create a superuser via Render Shell:
  ```bash
  python manage.py createsuperuser
  ```

### Important notes about media files

- On Render free/starter plans the filesystem is **ephemeral**.
- Uploaded images (avatars, receipts, goal images, attachments) will be lost on redeploy/restart.
- For production media you should use **Cloudinary**, **AWS S3**, or **Render Disk** (paid).
- The project is already configured with `MEDIA_URL` / `MEDIA_ROOT` so adding cloud storage later is straightforward.

### Checking logs

Dashboard → your web service → **Logs** tab.

---

## Project Structure

```
├── manage.py
├── requirements.txt
├── build.sh                 # Render build script
├── render.yaml              # Blueprint
├── .env.example
├── productivity_app/
│   ├── settings.py          # Production-ready settings
│   ├── urls.py
│   └── wsgi.py
├── accounts/                # Auth + dashboard + profile
├── tasks/
├── goals/
├── habits/
├── notes/
├── calendar_app/
├── expenses/
├── templates/               # Mobile-first HTML
├── static/css/style.css     # Responsive CSS
└── static/js/main.js
```

## Tech Stack

- Django 5.1+ / 6.x
- Gunicorn
- WhiteNoise (static files)
- PostgreSQL (via `dj-database-url` + `psycopg2-binary`)
- Pillow (images)
- Pure CSS mobile-first UI (no frontend framework needed)

---

## License

MIT – free to use and modify.
