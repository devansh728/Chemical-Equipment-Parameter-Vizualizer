# Installation & Deployment

### Prerequisites

- **Python**: 3.8 or higher
- **Node.js**: 16.x or higher (for web frontend)
- **Redis**: 6.x or higher
- **PostgreSQL**: 12.x or higher (production)
- **Docker**: 20.x or higher (optional, for containerized deployment)

### Development Setup

#### 1. Backend Setup

```bash
# Navigate to backend directory
cd chemical_visualizer/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your configuration:(REQUIRED)
# - SECRET_KEY
# - GEMINI_API_KEY
# - REDIS_URL

# Run database migrations
python manage.py makemigrtions ( if issue persists use "python manage.py makemigrations dataset" )
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start Django development server
python manage.py runserver
```

#### 2. Celery Worker Setup

```bash
# In a new terminal, activate virtual environment
cd chemical_visualizer/backend
venv\Scripts\activate  # or source venv/bin/activate

# Start Celery worker
celery -A backend worker --loglevel=info --pool=solo
```

#### 3. Redis Setup

```bash
# Install Redis
# Windows: Download from https://redis.io/download
# Linux: sudo apt-get install redis-server
# Mac: brew install redis

# Start Redis server
redis-server
```

#### 4. Web Frontend Setup

```bash
# Navigate to frontend directory
cd chemical_visualizer_frontend

# Install dependencies
npm install

# Configure environment variables
cp .env.example .env
# Edit .env with backend URL:
# VITE_API_BASE_URL=http://localhost:8000
# VITE_WS_BASE_URL=ws://localhost:8000

# Start development server
npm run dev

# Access at http://localhost:5173
```

#### 5. Desktop Application Setup

```bash
# Navigate to desktop app directory
cd desktop_app

# Option A: Quick Install (Windows)
install.bat

# Option B: Quick Install (Linux/Mac)
chmod +x install.sh
./install.sh

# Option C: Manual Installation
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with backend URL

# Run desktop application
python main.py
# Or use launcher:
run.bat  # Windows
./run.sh  # Linux/Mac
```

### Production Deployment (Docker)/ For Quick Backend StartUp

#### Using Docker Compose

```bash
# Navigate to project root
cd chemical_visualizer

# Build and start all services
docker compose up -d

# View logs
docker compose logs -f

# Stop all services
docker compose down

# Access services:
# - Web App: http://localhost:3000
# - Backend API: http://localhost:8000
# - Admin Panel: http://localhost:8000/admin
```

#### Docker Services

- **web**: Django application (Gunicorn)
- **celery**: Celery worker for async tasks
- **redis**: Redis server (message broker + cache)
- **db**: PostgreSQL database
- **frontend**: React application (Nginx)

---