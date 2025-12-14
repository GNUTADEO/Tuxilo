# Tuxilo Deployment Guide

Complete step-by-step guide to deploy the Tuxilo Hydrological System on any machine.

## Prerequisites

### Required Software
- **Docker** (version 20.10+)
- **Docker Compose** (version 2.0+)
- **Git**
- **Node.js** (version 18+) - Only needed for local development
- At least **4GB RAM** and **10GB disk space**

### System Requirements
- Linux, macOS, or Windows with WSL2
- Internet connection for initial setup
- Ports available: 5432, 5173, 8000, 8081

---

## Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd Tuxilo
```

---

## Step 2: Prepare Secrets

The system requires several secret files for security.

### 2.1 Create Secrets Directory Structure

```bash
mkdir -p App/Deploy-2/Secrets
```

### 2.2 Generate Required Secrets

#### PostgreSQL Password
```bash
echo "your_secure_password_here" > App/Deploy-2/Secrets/postgres_password
chmod 600 App/Deploy-2/Secrets/postgres_password
```

#### JWT Keys (for authentication)
```bash
# Generate Ed25519 key pair
ssh-keygen -t ed25519 -f App/Deploy-2/Secrets/jwt_private.pem -N ""
mv App/Deploy-2/Secrets/jwt_private.pem.pub App/Deploy-2/Secrets/jwt_public.pem
chmod 600 App/Deploy-2/Secrets/jwt_private.pem
chmod 644 App/Deploy-2/Secrets/jwt_public.pem
```

#### Fernet Key (optional, for encryption)
```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())" > App/Deploy-2/Secrets/fernet_password
```

---

## Step 3: Prepare Data Files

### 3.1 Ensure CSV Data Exists

Make sure the embalses data file exists:
```bash
ls -lh data/XM/EmbalsesColombia.csv
```

This file should contain reservoir data with columns: id, nombre, latitud, longitud.

### 3.2 Verify Init SQL Script

The database initialization script should be at:
```bash
ls -lh App/Deploy-2/init-db.sql
```

---

## Step 4: Configure Environment Variables

### 4.1 Review and Update .env File

Edit `App/Deploy-2/.env` and update these values:

```bash
cd App/Deploy-2
nano .env
```

Key variables to check:
```env
# Set to true for production
PRODUCTION_MODE=false

# Database credentials (must match secrets)
PG_DB_USER=postgres
PG_DB_NAME=tuxhydro

# Ports (change if conflicts exist)
PORT_DB_PG=5432
PORT_PGADMIN=8081
PORT_FRONT=5173
PORT_CORE=8000

# PgAdmin credentials
PGADMIN_DEFAULT_EMAIL=your_email@example.com
PGADMIN_DEFAULT_PASSWORD=your_secure_password

# CORS for production (update with your domain)
PUBLIC_ORIGINS=http://localhost:3000,http://your-domain.com
NODE_ORIGINS=http://localhost:3000
```

---

## Step 5: Build and Deploy

### 5.1 Build Docker Images

From the `App/Deploy-2` directory:

```bash
cd App/Deploy-2
docker-compose build
```

This will:
- Build the API backend container
- Build the frontend container
- Pull required base images (PostgreSQL, nginx, pgAdmin)

**Note**: First build may take 10-15 minutes.

### 5.2 Start All Services

```bash
docker-compose up -d
```

This starts:
- **gis_db**: PostgreSQL with PostGIS
- **tuxhydro_api_core**: FastAPI backend
- **tuxhydro_frontend**: SvelteKit frontend
- **nginx**: Reverse proxy
- **pgadmin**: Database management interface

### 5.3 Verify Services Are Running

```bash
docker-compose ps
```

All services should show "Up" or "healthy" status.

---

## Step 6: Verify Deployment

### 6.1 Check Database

```bash
# Connect to database
docker exec -it gis_db psql -U postgres -d tuxhydro

# Verify embalses table
\dt
SELECT COUNT(*) FROM embalses;
\q
```

### 6.2 Check API

```bash
# Test API endpoint
curl http://localhost:8000/public/embalses/ | jq
```

Should return JSON with embalses data.

### 6.3 Check Frontend

Open your browser to:
- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **pgAdmin**: http://localhost:8081

---

## Step 7: Access the Application

### Main Application
- URL: http://localhost:5173
- You should see:
  - Map with reservoir markers
  - Dropdown to select embalses
  - Controls sidebar
  - Time series chart

### API Documentation
- URL: http://localhost:8000/docs
- Interactive API documentation (Swagger UI)

### Database Management
- URL: http://localhost:8081
- Login with credentials from `.env`
- Add server:
  - Host: `gis_db`
  - Port: `5432`
  - User: `postgres`
  - Password: (from secrets file)
  - Database: `tuxhydro`

---

## Step 8: Production Deployment

For production deployment on a server:

### 8.1 Update Configuration

```bash
# Edit .env
PRODUCTION_MODE=true
PUBLIC_ORIGINS=https://your-domain.com
```

### 8.2 Set Up SSL/TLS

Update `nginx.conf` to add SSL certificates:

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    # ... rest of config
}
```

### 8.3 Use Production Build

For frontend, switch to production Dockerfile:

```yaml
# In compose.yaml
frontend:
  build:
    dockerfile: Dockerfile  # Instead of Dockerfile.dev
```

### 8.4 Set Up Backups

```bash
# Database backup script
docker exec gis_db pg_dump -U postgres tuxhydro > backup_$(date +%Y%m%d).sql
```

---

## Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose logs -f

# Check specific service
docker logs tuxhydro_api_core
docker logs tuxhydro_frontend
docker logs gis_db
```

### Port Conflicts

```bash
# Find what's using a port
sudo lsof -i :5432
sudo lsof -i :8000

# Change ports in .env file
```

### Database Connection Issues

```bash
# Check database is healthy
docker exec gis_db pg_isready -U postgres

# Check network connectivity
docker exec tuxhydro_api_core ping gis_db
```

### Frontend Not Loading Map

1. Check API is accessible: `curl http://localhost:8000/public/embalses/`
2. Open browser console (F12) for JavaScript errors
3. Check CORS settings in `.env`

### Rebuild After Code Changes

```bash
# Rebuild specific service
docker-compose build api_core
docker-compose up -d api_core

# Rebuild all
docker-compose down
docker-compose build
docker-compose up -d
```

---

## Maintenance Commands

### Stop All Services
```bash
docker-compose down
```

### Stop and Remove Volumes (⚠️ Deletes Data)
```bash
docker-compose down -v
```

### Update Application
```bash
git pull
docker-compose build
docker-compose up -d
```

### View Logs
```bash
docker-compose logs -f
docker-compose logs -f frontend
docker-compose logs -f api_core
```

### Restart Service
```bash
docker-compose restart frontend
docker-compose restart api_core
```

---

## Architecture Summary

```
┌─────────────────────────────────────────────────┐
│                   Browser                        │
│         http://localhost:5173                    │
└───────────────────┬─────────────────────────────┘
                    │
        ┌───────────▼───────────┐
        │  Frontend (SvelteKit) │
        │  Port: 5173           │
        └───────────┬───────────┘
                    │ fetch()
        ┌───────────▼───────────┐
        │  API (FastAPI)        │
        │  Port: 8000           │
        └───────────┬───────────┘
                    │ SQL queries
        ┌───────────▼───────────┐
        │  PostgreSQL + PostGIS │
        │  Port: 5432           │
        └───────────────────────┘
```

---

## Security Notes

⚠️ **Important for Production:**

1. Change all default passwords
2. Use strong, unique passwords for database and pgAdmin
3. Enable SSL/TLS for all connections
4. Restrict CORS origins to your domain only
5. Keep secrets files secure (never commit to git)
6. Regularly update Docker images
7. Set up firewall rules
8. Use environment-specific .env files

---

## Support

For issues or questions:
- Check logs: `docker-compose logs`
- Review this guide's Troubleshooting section
- Check Docker and Docker Compose documentation

---

**Last Updated**: December 14, 2024
**Version**: 1.0.0
