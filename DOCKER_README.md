# SME Financial Health Platform - Docker Setup

## Quick Start

### Prerequisites
- Docker Desktop installed
- Docker Compose v2+

### Run the Application

```bash
# Clone and navigate to project
cd AAAGuvi

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Access the Application

| Service | URL |
|---------|-----|
| Frontend | http://localhost |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| DB Admin | http://localhost:8000/admin |

## Services

### 1. Database (PostgreSQL)
- **Image:** `postgres:15-alpine`
- **Port:** 5432
- **Volume:** `postgres_data` (persistent)

### 2. Backend (FastAPI)
- **Port:** 8000
- **Hot Reload:** Enabled for development
- **Dependencies:** Python 3.11

### 3. Frontend (React + Nginx)
- **Port:** 80
- **Proxy:** API requests → Backend

## Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build

# View logs
docker-compose logs -f backend

# Access backend shell
docker exec -it sme_backend bash

# Access database
docker exec -it sme_db psql -U postgres -d financial_health

# Remove all data (including volumes)
docker-compose down -v
```

## Environment Variables

Create `.env` file in root directory:

```env
# Database
DB_PASSWORD=postgres123

# Security
SECRET_KEY=your-secret-key-here
ENCRYPTION_KEY=32-character-encryption-key!

# LLM (Groq)
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
```

## Architecture

```
┌─────────────────────────────────────────────────┐
│                    Docker Network               │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────┐     ┌──────────┐    ┌──────────┐ │
│  │ Frontend │────▶│ Backend  │───▶│   DB     │ │
│  │  (Nginx) │     │ (FastAPI)│    │(Postgres)│ │
│  │  :80     │     │  :8000   │    │  :5432   │ │
│  └──────────┘     └──────────┘    └──────────┘ │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Production Deployment

For production, modify `docker-compose.yml`:

1. Remove `--reload` from backend command
2. Use production environment variables
3. Add SSL/TLS certificates to nginx
4. Set up proper volume backups

```yaml
# Production backend command
command: uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Troubleshooting

### Backend won't start
```bash
# Check logs
docker-compose logs backend

# Verify database connection
docker exec -it sme_backend python -c "from database import engine; print(engine.url)"
```

### Frontend shows blank page
```bash
# Rebuild frontend
docker-compose up -d --build frontend
```

### Database connection refused
```bash
# Wait for DB to be healthy
docker-compose ps  # Check health status
```

---

*Last updated: February 2026*
