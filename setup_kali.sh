#!/bin/bash
# VAPT Scanner - Kali Linux Setup Script
# This script sets up the VAPT Scanner vulnerability assessment platform on Kali Linux

set -e

echo "=========================================="
echo "VAPT Scanner - Kali Linux Setup"
echo "=========================================="

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running on Kali Linux
if ! grep -qi kali /etc/os-release 2>/dev/null; then
    echo -e "${YELLOW}Warning: This script is optimized for Kali Linux${NC}"
fi

# Step 1: Update system packages
echo -e "${GREEN}[1/7] Updating system packages...${NC}"
sudo apt-get update
sudo apt-get upgrade -y

# Step 2: Install system dependencies
echo -e "${GREEN}[2/7] Installing system dependencies...${NC}"
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    git \
    build-essential \
    libssl-dev \
    libffi-dev \
    postgresql-client \
    libpq-dev \
    nmap \
    nikto \
    zaproxy \
    bandit \
    semgrep \
    libmagic1 \
    docker.io

# Step 3: Create Python virtual environment
echo -e "${GREEN}[3/7] Creating Python virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created"
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate

# Step 4: Upgrade pip and install requirements
echo -e "${GREEN}[4/7] Installing Python dependencies...${NC}"
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Step 5: Database setup
echo -e "${GREEN}[5/7] Setting up database...${NC}"
# Check if PostgreSQL is running
if ! systemctl is-active --quiet postgresql; then
    echo -e "${YELLOW}PostgreSQL not running. Installing and starting...${NC}"
    sudo apt-get install -y postgresql postgresql-contrib
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
fi

# Create database and user if they don't exist
DB_NAME="vapt_db"
DB_USER="vapt_user"
DB_PASSWORD="vapt_secure_password"

sudo -u postgres psql <<-EOSQL
    SELECT 1 FROM pg_database WHERE datname = '${DB_NAME}' || exit 0
    CREATE DATABASE ${DB_NAME};
    CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';
    ALTER ROLE ${DB_USER} SET client_encoding TO 'utf8';
    ALTER ROLE ${DB_USER} SET default_transaction_isolation TO 'read committed';
    ALTER ROLE ${DB_USER} SET default_transaction_deferrable TO on;
    ALTER ROLE ${DB_USER} SET default_transaction_level TO 'read committed';
    ALTER ROLE ${DB_USER} SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};
EOSQL

# Step 6: Configure Django settings
echo -e "${GREEN}[6/7] Configuring Django...${NC}"

# Create .env file for environment variables
if [ ! -f ".env" ]; then
    cat > .env << EOF
DJANGO_DEBUG=0
DJANGO_SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@localhost:5432/${DB_NAME}
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
EOF
    echo "Created .env file"
fi

# Load environment variables
export $(cat .env | xargs)

# Run migrations
python manage.py migrate
echo -e "${GREEN}Migrations completed${NC}"

# Create superuser (optional - you can do this interactively)
echo -e "${YELLOW}Creating superuser...${NC}"
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

# Collect static files
python manage.py collectstatic --noinput

# Step 7: Install and configure scanning tools
echo -e "${GREEN}[7/7] Installing scanning tools...${NC}"

# Check for OWASP ZAP
if ! command -v zaproxy &> /dev/null; then
    echo -e "${YELLOW}Installing OWASP ZAP...${NC}"
    sudo apt-get install -y zaproxy
fi

# Check for gvm-tools (for OpenVAS)
if ! pip list | grep -q gvm-tools; then
    echo -e "${YELLOW}Installing gvm-tools for OpenVAS...${NC}"
    pip install gvm-tools
fi

# Verify checker
echo -e "${GREEN}Verifying installations...${NC}"
python -c "import django; print(f'Django {django.get_version()} ✓')"
command -v nmap &> /dev/null && echo "Nmap ✓" || echo "Nmap ✗"
command -v nikto &> /dev/null && echo "Nikto ✓" || echo "Nikto ✗"
command -v zaproxy &> /dev/null && echo "OWASP ZAP ✓" || echo "OWASP ZAP ✗"
pip list | grep -q bandit && echo "Bandit ✓" || echo "Bandit ✗"
pip list | grep -q semgrep && echo "Semgrep ✓" || echo "Semgrep ✗"

echo ""
echo "=========================================="
echo -e "${GREEN}Setup completed successfully!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Start the development server:"
echo "   python manage.py runserver 0.0.0.0:8000"
echo ""
echo "3. Or start with Gunicorn (production):"
echo "   gunicorn -w 4 -b 0.0.0.0:8000 vapt.wsgi --timeout 300"
echo ""
echo "4. Access the application:"
echo "   http://localhost:8000/"
echo "   Admin panel: http://localhost:8000/admin/"
echo ""
echo "5. Default credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "=========================================="
