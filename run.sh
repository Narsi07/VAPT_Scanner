#!/bin/bash

echo "[VAPT] Starting VAPT Scanner on Kali Linux..."

# ── 1. Start PostgreSQL ───────────────────────────────────────────────────────
echo "[VAPT] Checking PostgreSQL..."
if ! pg_isready -h 127.0.0.1 -p 5432 -q; then
    echo "[VAPT] Starting PostgreSQL service..."
    sudo service postgresql start
    sleep 3
fi

if ! pg_isready -h 127.0.0.1 -p 5432 -q; then
    echo "[VAPT ERROR] PostgreSQL failed to start. Please run: sudo service postgresql start"
    exit 1
fi
echo "[VAPT] PostgreSQL is running."

# ── 2. Create database and user if they don't exist ──────────────────────────
echo "[VAPT] Setting up database..."
sudo -u postgres psql -tc "SELECT 1 FROM pg_user WHERE usename='vaptuser';" | grep -q 1 || \
    sudo -u postgres psql -c "CREATE USER vaptuser WITH PASSWORD 'vaptpass';"

sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname='vaptdb';" | grep -q 1 || \
    sudo -u postgres psql -c "CREATE DATABASE vaptdb OWNER vaptuser;"

sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE vaptdb TO vaptuser;" 2>/dev/null

# ── 3. Run Django migrations ──────────────────────────────────────────────────
echo "[VAPT] Running database migrations..."
python manage.py migrate --run-syncdb 2>&1 | tail -5

# ── 4. Start Gunicorn ─────────────────────────────────────────────────────────
echo "[VAPT] Starting Gunicorn on http://0.0.0.0:8000 ..."
export DJANGO_DEBUG=1
exec gunicorn \
    -b 0.0.0.0:8000 \
    vapt.wsgi:application \
    --worker-class gthread \
    --workers 1 \
    --threads 10 \
    --timeout 1800 \
    --control /home/kali/Downloads/VAPT_Scanner/gunicorn.ctl
